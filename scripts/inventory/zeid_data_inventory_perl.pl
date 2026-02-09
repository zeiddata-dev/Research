#!/usr/bin/env perl
use strict; use warnings;

sub run_cmd { my (@cmd)=@_; my $out = qx{@cmd 2>&1}; return $out // ""; }
sub now_iso {
  my @t=gmtime(); return sprintf("%04d-%02d-%02dT%02d:%02d:%02dZ",$t[5]+1900,$t[4]+1,$t[3],$t[2],$t[1],$t[0]);
}
sub ipv4_to_u32 {
  my ($ip)=@_; my @p=split(/\./,$ip); return undef unless @p==4;
  for my $b (@p){ return undef unless $b =~ /^\d+$/ && $b>=0 && $b<=255; }
  return ($p[0]<<24)|($p[1]<<16)|($p[2]<<8)|$p[3];
}
sub u32_to_ipv4 { my ($u)=@_; return sprintf("%d.%d.%d.%d",($u>>24)&255,($u>>16)&255,($u>>8)&255,$u&255); }
sub iter_hosts {
  my ($cidr)=@_; my ($base,$prefix)=split(/\//,$cidr);
  die "Invalid CIDR\n" unless defined $base && defined $prefix;
  die "Refusing prefix /$prefix (use /8..../30)\n" if $prefix<8 || $prefix>30;
  my $base_u=ipv4_to_u32($base); die "Invalid IPv4\n" unless defined $base_u;
  my $mask = $prefix==0 ? 0 : ((0xFFFFFFFF << (32-$prefix)) & 0xFFFFFFFF);
  my $net = $base_u & $mask; my $bcast = $net | ((~$mask) & 0xFFFFFFFF);
  my $start = $net + 1; my $end = $bcast - 1;
  my $count = $end - $start + 1; die "Refusing to scan $count hosts\n" if $count > 4096;
  my @hosts; for (my $u=$start;$u<=$end;$u++){ push @hosts, u32_to_ipv4($u); } return @hosts;
}
sub ping_one {
  my ($ip)=@_;
  if ($^O =~ /MSWin32/) { my $o=run_cmd("ping","-n","1","-w","750",$ip); return $o =~ /TTL=/i ? 1:0; }
  else { my $o=run_cmd("ping","-c","1","-W","1",$ip); return $o =~ /1 received|bytes from/i ? 1:0; }
}
sub parse_neighbors {
  my %recs;
  if ($^O =~ /MSWin32/) {
    my $out=run_cmd("arp","-a");
    for my $line (split(/\r?\n/,$out)){
      $line =~ s/^\s+|\s+$//g;
      next if $line eq "" || $line =~ /^Interface:/i || $line =~ /^Internet Address/i;
      my @p=split(/\s+/,$line); next unless @p>=2;
      my ($ip,$mac)=@p[0,1]; next unless defined ipv4_to_u32($ip);
      $mac =~ s/-/:/g; $recs{$ip}={ ip=>$ip, mac=>lc($mac), seen_via=>"arp" };
    }
  } else {
    my $out=run_cmd("ip","neigh");
    if ($out =~ /\S/) {
      for my $line (split(/\r?\n/,$out)){
        my @p=split(/\s+/,$line); next unless @p>=2;
        my $ip=$p[0]; next unless defined ipv4_to_u32($ip);
        my $mac=""; for (my $i=0;$i<@p-1;$i++){ $mac=lc($p[$i+1]) if $p[$i] eq "lladdr"; }
        $recs{$ip}={ ip=>$ip, mac=>$mac, seen_via=>"neigh" };
      }
    } else {
      my $out2=run_cmd("arp","-an");
      for my $line (split(/\r?\n/,$out2)){
        if ($line =~ /\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:]{17})/i) {
          $recs{$1}={ ip=>$1, mac=>lc($2), seen_via=>"arp" };
        }
      }
    }
  }
  return %recs;
}

my $subnet=""; my $active=0; my $out="inventory.csv";
for (my $i=0;$i<@ARGV;$i++){
  $subnet = $ARGV[$i+1] // "" if $ARGV[$i] eq "--subnet";
  $active = 1 if $ARGV[$i] eq "--active";
  $out = $ARGV[$i+1] // $out if $ARGV[$i] eq "--out";
}

my $ts=now_iso();
my %records=parse_neighbors();
my %reachable;

if ($active) {
  die "ERROR: --active requires --subnet\n" if $subnet eq "";
  my @hosts=iter_hosts($subnet);
  for my $ip (@hosts){
    my $ok=ping_one($ip); $reachable{$ip}=$ok;
    $records{$ip}={ ip=>$ip, mac=>"", seen_via=>"ping" } if $ok && !exists $records{$ip};
  }
  my %post=parse_neighbors();
  for my $ip (keys %post){
    if (exists $records{$ip}){
      $records{$ip}->{mac} = $post{$ip}->{mac} if (($records{$ip}->{mac}//"") eq "" && ($post{$ip}->{mac}//"") ne "");
      $records{$ip}->{seen_via} = $post{$ip}->{seen_via} if (($records{$ip}->{seen_via}//"") eq "ping");
    } else { $records{$ip}=$post{$ip}; }
  }
}

open(my $fh, ">", $out) or die "Cannot write $out\n";
print $fh "ip,mac,reachable,seen_via,timestamp\n";
for my $ip (sort keys %records){
  my $r=$records{$ip};
  my $reach_s="";
  $reach_s = $reachable{$ip} ? "1":"0" if ($active && exists $reachable{$ip});
  print $fh join(",", $ip, ($r->{mac}//""), $reach_s, ($r->{seen_via}//""), $ts) . "\n";
}
close($fh);
print "Wrote " . scalar(keys %records) . " record(s) to $out\n";
