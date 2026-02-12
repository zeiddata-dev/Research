// zeid_data_log_summarizer.cpp
//
// Counts occurrences of tokens in a log file and outputs JSON.
// Default tokens: ERROR,WARN,INFO,DEBUG
//
// Because reading logs manually is how you lose weekends.

#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>

static void usage() {
    std::cerr << "zeid_data_log_summarizer --in <file> [--out summary.json] [--tokens CSV]\n";
}

static std::vector<std::string> split_csv(const std::string& s) {
    std::vector<std::string> out;
    std::string cur;
    std::istringstream iss(s);
    while(std::getline(iss, cur, ',')) if(!cur.empty()) out.push_back(cur);
    return out;
}

static std::string json_escape(const std::string& s) {
    std::ostringstream o;
    for(char c : s) {
        switch(c){
            case '"': o << "\\\""; break;
            case '\\': o << "\\\\"; break;
            case '\n': o << "\\n"; break;
            case '\r': o << "\\r"; break;
            case '\t': o << "\\t"; break;
            default: o << c;
        }
    }
    return o.str();
}

int main(int argc, char** argv){
    std::string in_path;
    std::string out_path = "summary.json";
    std::vector<std::string> tokens = {"ERROR","WARN","INFO","DEBUG"};

    for(int i=1;i<argc;i++){
        std::string a = argv[i];
        if(a == "--in" && i+1<argc) in_path = argv[++i];
        else if(a == "--out" && i+1<argc) out_path = argv[++i];
        else if(a == "--tokens" && i+1<argc) tokens = split_csv(argv[++i]);
        else { usage(); return 2; }
    }
    if(in_path.empty()){ usage(); return 2; }

    std::ifstream in(in_path);
    if(!in){ std::cerr << "ERROR: cannot read input: " << in_path << "\n"; return 2; }

    std::map<std::string, long long> counts;
    for(const auto& t : tokens) counts[t] = 0;

    long long lines = 0;
    std::string line;
    while(std::getline(in, line)){
        lines++;
        for(const auto& t : tokens){
            if(line.find(t) != std::string::npos) counts[t] += 1;
        }
    }

    std::ofstream out(out_path);
    if(!out){ std::cerr << "ERROR: cannot write output: " << out_path << "\n"; return 2; }

    out << "{\n";
    out << "  \"input\": \"" << json_escape(in_path) << "\",\n";
    out << "  \"lines\": " << lines << ",\n";
    out << "  \"counts\": {\n";
    bool first = true;
    for(const auto& kv : counts){
        if(!first) out << ",\n";
        first = false;
        out << "    \"" << json_escape(kv.first) << "\": " << kv.second;
    }
    out << "\n  }\n";
    out << "}\n";

    std::cout << "Wrote: " << out_path << " (lines=" << lines << ")\n";
    return 0;
}
