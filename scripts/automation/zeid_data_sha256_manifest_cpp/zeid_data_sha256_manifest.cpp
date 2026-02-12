// zeid_data_sha256_manifest.cpp
//
// Generates a SHA-256 manifest for files in a directory.
// Output: CSV (path,size,sha256,status)
//
// Build (Linux/macOS):
//   g++ -std=c++17 -O2 -o zeid_data_sha256_manifest zeid_data_sha256_manifest.cpp
//
// Build (Windows, MSVC):
//   cl /std:c++17 /O2 zeid_data_sha256_manifest.cpp
//
// Usage:
//   ./zeid_data_sha256_manifest --dir ./artifacts --out manifest.csv

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>


#include <array>
#include <cstdint>
#include <cstring>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

struct Sha256 {
    std::array<uint32_t, 8> h{
        0x6a09e667u,0xbb67ae85u,0x3c6ef372u,0xa54ff53au,0x510e527fu,0x9b05688cu,0x1f83d9abu,0x5be0cd19u
    };
    std::array<uint8_t, 64> buf{};
    uint64_t bits = 0;
    size_t len = 0;

    static uint32_t rotr(uint32_t x, uint32_t n){ return (x>>n) | (x<<(32-n)); }
    static uint32_t ch(uint32_t x,uint32_t y,uint32_t z){ return (x & y) ^ (~x & z); }
    static uint32_t maj(uint32_t x,uint32_t y,uint32_t z){ return (x & y) ^ (x & z) ^ (y & z); }
    static uint32_t bsig0(uint32_t x){ return rotr(x,2) ^ rotr(x,13) ^ rotr(x,22); }
    static uint32_t bsig1(uint32_t x){ return rotr(x,6) ^ rotr(x,11) ^ rotr(x,25); }
    static uint32_t ssig0(uint32_t x){ return rotr(x,7) ^ rotr(x,18) ^ (x>>3); }
    static uint32_t ssig1(uint32_t x){ return rotr(x,17) ^ rotr(x,19) ^ (x>>10); }

    static constexpr std::array<uint32_t, 64> k = {
        0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,
        0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,
        0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
        0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,
        0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,
        0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
        0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,
        0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u
    };

    void compress(const uint8_t block[64]) {
        uint32_t w[64];
        for(int i=0;i<16;i++){
            w[i] = (uint32_t(block[i*4])<<24) | (uint32_t(block[i*4+1])<<16) | (uint32_t(block[i*4+2])<<8) | uint32_t(block[i*4+3]);
        }
        for(int i=16;i<64;i++){
            w[i] = ssig1(w[i-2]) + w[i-7] + ssig0(w[i-15]) + w[i-16];
        }

        uint32_t a=h[0],b=h[1],c=h[2],d=h[3],e=h[4],f=h[5],g=h[6],hh=h[7];

        for(int i=0;i<64;i++){
            uint32_t t1 = hh + bsig1(e) + ch(e,f,g) + k[i] + w[i];
            uint32_t t2 = bsig0(a) + maj(a,b,c);
            hh=g; g=f; f=e; e=d+t1; d=c; c=b; b=a; a=t1+t2;
        }

        h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d; h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }

    void update(const uint8_t* data, size_t n){
        bits += uint64_t(n) * 8;
        while(n){
            size_t take = std::min(n, 64 - len);
            std::memcpy(buf.data()+len, data, take);
            len += take;
            data += take;
            n -= take;
            if(len == 64){
                compress(buf.data());
                len = 0;
            }
        }
    }

    std::string final_hex(){
        buf[len++] = 0x80;
        if(len > 56){
            while(len < 64) buf[len++] = 0;
            compress(buf.data());
            len = 0;
        }
        while(len < 56) buf[len++] = 0;

        for(int i=7;i>=0;i--){
            buf[len++] = uint8_t((bits >> (i*8)) & 0xff);
        }
        compress(buf.data());

        std::ostringstream oss;
        for(auto v : h){
            oss << std::hex << std::setfill('0') << std::setw(8) << v;
        }
        return oss.str();
    }
};


namespace fs = std::filesystem;

static bool hash_file(const fs::path& p, std::string& out_hex, uintmax_t& out_size, std::string& err) {
    std::ifstream in(p, std::ios::binary);
    if(!in){ err = "open_failed"; return false; }
    Sha256 sha;
    std::vector<uint8_t> buf(1 << 16);
    uintmax_t total = 0;

    while(in){
        in.read(reinterpret_cast<char*>(buf.data()), static_cast<std::streamsize>(buf.size()));
        std::streamsize got = in.gcount();
        if(got > 0){
            sha.update(buf.data(), static_cast<size_t>(got));
            total += static_cast<uintmax_t>(got);
        }
    }
    out_hex = sha.final_hex();
    out_size = total;
    return true;
}

static void usage() {
    std::cerr << "zeid_data_sha256_manifest --dir <path> --out <file>\n";
}

int main(int argc, char** argv){
    fs::path dir;
    fs::path out = "manifest.csv";

    for(int i=1;i<argc;i++){
        std::string a = argv[i];
        if(a == "--dir" && i+1<argc){ dir = argv[++i]; }
        else if(a == "--out" && i+1<argc){ out = argv[++i]; }
        else { usage(); return 2; }
    }
    if(dir.empty() || !fs::exists(dir)){
        std::cerr << "ERROR: --dir must exist\n";
        return 2;
    }

    std::ofstream csv(out);
    if(!csv){
        std::cerr << "ERROR: cannot write output: " << out << "\n";
        return 2;
    }
    csv << "path,size_bytes,sha256,status\n";

    size_t ok = 0, fail = 0;

    for(auto it = fs::recursive_directory_iterator(dir); it != fs::recursive_directory_iterator(); ++it){
        const auto& p = it->path();
        if(it->is_directory()) continue;
        if(!it->is_regular_file()) continue;

        std::string hex, err;
        uintmax_t size = 0;
        bool good = hash_file(p, hex, size, err);

        fs::path rel = p;
        try { rel = fs::relative(p, dir); } catch(...) {}

        if(good){
            csv << rel.generic_string() << "," << size << "," << hex << ",ok\n";
            ok++;
        } else {
            csv << rel.generic_string() << ",,," << err << "\n";
            fail++;
        }
    }

    std::cout << "Wrote: " << out << " (ok=" << ok << ", fail=" << fail << ")\n";
    return (fail == 0) ? 0 : 1;
}
