
#include<iostream>
#include <utility>
#include <bitset>
#include <cstdint>
#include <string>
#include <vector>
#include <sstream>
#include <iomanip>
#include <chrono>
using namespace std;
#define u_32 unsigned int
string IV = "7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e";
string strTobin(const string& input) {
    unsigned char tmp;
    string res;
    for (char c : input) {
        tmp = static_cast<int>(c);
        res.append(bitset<8>(tmp).to_string());
    }
    return res;
}

string padding(const string& input, int length) {
    string paddingString(length, '0');
    return input + paddingString;
}

string dtoh(u_32 n) {
    stringstream ss;
    ss << hex << setw(8) << setfill('0') << n;
    return ss.str();
}

u_32 circleLS(u_32 input, int n) {
    return (input << n) | (input >> (32 - n));
}

u_32 T(int j) {
    if (j >= 0 && j <= 15)
        return u_32(stoul("79cc4519", nullptr, 16));
    else
        return u_32(stoul("7a879d8a", nullptr, 16));
}

u_32 FF(u_32 x, u_32 y, u_32 z, int j) {
    if (j >= 0 && j <= 15)
        return x ^ y ^ z;
    else
        return (x & y) | (x & z) | (y & z);
}

u_32 GG(u_32 x, u_32 y, u_32 z, int j) {
    if (j >= 0 && j <= 15)
        return x ^ y ^ z;
    else
        return (x & y) | (~x & z);
}

u_32 P0(u_32 input) {
    return input ^ circleLS(input, 9) ^ circleLS(input, 17);
}

u_32 P1(u_32 input) {
    return input ^ circleLS(input, 15) ^ circleLS(input, 23);
}

string messagePadding(string message) {
    string M_bin = strTobin(move(message));

    int len = M_bin.length();
    string padOfLen = bitset<32>(len).to_string();
    string zeroString(64 - padOfLen.length(), '0');
    padOfLen = zeroString + padOfLen;

    int zeroLen;
    if ((len + 1) % 512 <= 448) zeroLen = 448 - len - 1;
    else
        zeroLen = 512 - len + 448 - 1;

    M_bin += "1";
    string M = padding(M_bin, zeroLen);
    M += padOfLen;

    return M;
}

vector<u_32> Extending(const string& group) {
    vector<u_32> W;
    vector<u_32> W_;

    string tmp;
    for (int j = 0; j < 16; j++) {
        tmp = group.substr(j * 32, 32);
        W.push_back(stoul(tmp, nullptr, 2));
    }

    u_32 tmp1, tmp2, tmp3;
    for (int j = 16; j < 68; j++) {
        tmp1 = P1(W[j - 16] ^ W[j - 9] ^ circleLS(W[j - 3], 15));
        tmp2 = circleLS(W[j - 13], 7);
        tmp3 = W[j - 6];
        W.push_back(tmp1 ^ tmp2 ^ tmp3);
    }

    for (int j = 0; j < 64; j++)
        W_.push_back(W[j] ^ W[j + 4]);

    W.insert(W.end(), W_.begin(), W_.end());

    return W;
}

string CF(const string& V_i, vector<u_32> B_i) {
    u_32 A = u_32(stoul(V_i.substr(0, 8), nullptr, 16));
    u_32 B = u_32(stoul(V_i.substr(8, 8), nullptr, 16));
    u_32 C = u_32(stoul(V_i.substr(16, 8), nullptr, 16));
    u_32 D = u_32(stoul(V_i.substr(24, 8), nullptr, 16));
    u_32 E = u_32(stoul(V_i.substr(32, 8), nullptr, 16));
    u_32 F = u_32(stoul(V_i.substr(40, 8), nullptr, 16));
    u_32 G = u_32(stoul(V_i.substr(48, 8), nullptr, 16));
    u_32 H = u_32(stoul(V_i.substr(56, 8), nullptr, 16));
    u_32 A_ = u_32(stoul(V_i.substr(0, 8), nullptr, 16));
    u_32 B_ = u_32(stoul(V_i.substr(8, 8), nullptr, 16));
    u_32 C_ = u_32(stoul(V_i.substr(16, 8), nullptr, 16));
    u_32 D_ = u_32(stoul(V_i.substr(24, 8), nullptr, 16));
    u_32 E_ = u_32(stoul(V_i.substr(32, 8), nullptr, 16));
    u_32 F_ = u_32(stoul(V_i.substr(40, 8), nullptr, 16));
    u_32 G_ = u_32(stoul(V_i.substr(48, 8), nullptr, 16));
    u_32 H_ = u_32(stoul(V_i.substr(56, 8), nullptr, 16));

    u_32 SS1, SS2, TT1, TT2;
    for (int j = 0; j < 64; j++) {
        SS1 = circleLS(circleLS(A, 12) + E + circleLS(T(j), j), 7);
        SS2 = SS1 ^ circleLS(A, 12);
        TT1 = FF(A, B, C, j) + D + SS2 + B_i[68 + j];
        TT2 = GG(E, F, G, j) + H + SS1 + B_i[j];
        D = C;
        C = circleLS(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = circleLS(F, 19);
        F = E;
        E = P0(TT2);
    }
    string a = dtoh(A ^ A_);
    string b = dtoh(B ^ B_);
    string c = dtoh(C ^ C_);
    string d = dtoh(D ^ D_);
    string e = dtoh(E ^ E_);
    string f = dtoh(F ^ F_);
    string g = dtoh(G ^ G_);
    string h = dtoh(H ^ H_);

    return a + b + c + d + e + f + g + h;
}

string hashsm3(string message) {
    string M_bin = messagePadding(message);

    int blockNum = M_bin.length() / 512;
    vector<vector<u_32>> B;
    B.reserve(blockNum);
    for (int i = 0; i < blockNum; i++) {
        string group = M_bin.substr(i * 512, 512);
        B.emplace_back(Extending(group));
    }

    string V = IV;
    for (int i = 0; i < blockNum; i++)
        V = CF(V, B[i]);

    return V;
}
int main() {
    string data = "encryption!";
   
     
    string hashValue;
    auto t1 = chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000; i++)
        hashValue = hashsm3(data);
    auto t2 = chrono::high_resolution_clock::now();
    auto t3 = chrono::duration_cast<chrono::milliseconds>(t2 - t1);
    //因为一次加密时间接近0，所以直接加密10000次算平均值
    cout << "消息: " << data << '\n';
    cout << "哈希值: " << hashValue << '\n';
    cout << "10000次加密所用时间: " << t3.count() << "ms\n";
    cout << "平均每次加密所用时间: " << t3.count() / double(1000000) << "ms\n";

    return 0;
}
