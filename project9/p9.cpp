#include<iostream>
#include<string>
#include<vector>
#include <chrono>
using namespace std;

// s 盒
static const int S[16][16] = { 0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
	0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
	0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
	0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
	0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
	0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
	0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
	0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
	0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
	0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
	0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
	0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
	0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
	0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
	0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
	0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 };

// 常量轮值表
static const long long Rcon[10] = {
	0x01000000, 0x02000000,0x04000000, 0x08000000,0x10000000, 0x20000000,0x40000000, 0x80000000,0x1b000000, 0x36000000
};

int Int(char& ch)//单个字符转为十六进制数
{
	int num = 0;
	if (ch >= 48 && ch <= 57)
	{
		num = ch - 48;
	}
	else if (ch >= 97 && ch <= 102)
	{
		num = ch - 87;
	}
	return num;
}

long long strInt(string str)//字符串转化为十六进制数
{
	long long num = 0;
	for (char ch : str)
	{
		num *= 16;
		num += Int(ch);
	}
	return num;
}

string Char(long long num)//十六进制数转为字符串
{
	string str = "";
	while (num)
	{
		int x = num & 0xf;
		if (x <= 9)
		{
			char ch = x + 48;
			str += ch;
		}
		else
		{
			char ch = x + 87;
			str += ch;
		}
		num >>= 4;
	}
	int x = str.length();
	for (int i = 0; i < x / 2; i++)
	{
		char temp = str[i];
		str[i] = str[x - i - 1];
		str[x - i - 1] = temp;
	}
	return str;
}

vector<string> MakeGroup(string& key)//使用动态数组将128位16进制数分为4组32位16进制数
{
	vector<string> groups(4);
	int index = 0;
	for (string& g : groups)
	{
		g = key.substr(index, 8);
		index += 8;
	}
	return groups;
}

string G(string& r_key, int round)//密钥拓展中的g函数
{
	string str = r_key.substr(2) + r_key.substr(0, 2);
	int len = r_key.length();
	for (int i = 0; i < len; i += 2)
	{
		int x = Int(str[i]);
		int y = Int(str[i + 1]);
		string temp = Char(S[x][y]);
		if (temp.length() < 2)
			temp = "0" + temp;
		str[i] = temp[0];
		str[i + 1] = temp[1];
	}
	long long num = strInt(str);
	num ^= Rcon[round];
	string str1 = Char(num);
	while (str1.length() < 8)
		str1 = "0" + str1;

	return str1;
}

string strXor(string s1, string s2)//8位16进制字符串异或
{
	long long num1 = strInt(s1), num2 = strInt(s2);
	long long num = num1 ^ num2;
	string str = Char(num);
	while (str.length() < 8)
		str = "0" + str;
	return str;
}


vector<string> KeyExtend(string& key0)//计算十轮拓展密钥
{
	vector<string> key = MakeGroup(key0);
	for (int i = 4; i < 44; i++)
	{
		string k = "";
		string temp = key[i - 1];
		if (i % 4 == 0)
			temp = G(temp, i / 4 - 1);
		k = strXor(temp, key[i - 4]);
		key.push_back(k);
	}
	return key;
}

vector<string> RowMove(vector<string>& s)//行移位
{
	vector<string> str = s;
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			str[j][2*i] = s[(j + i) % 4][2*i];
			str[j][2*i + 1] = s[(j + i) % 4][2*i + 1];
		}
	}
	return str;
}

vector<string> split_s(string& s)//将2位十六进制数视为一组
{
	vector<string> ans;
	for (int i = 0; i < s.length(); i += 2)
	{
		ans.emplace_back(s.substr(i, 2));
	}
	return ans;
}

int LeftShift(int num)//{02}*Si,c运算
{
	int ans = (num << 1) % 0b100000000;
	if (num & 0b10000000)
		ans ^= 0b00011011;
	return ans;
}

vector<string> ColConfuse(vector<string>& s)//列混淆
{
	vector<string> str = s;
	for (int i = 0; i < 4; ++i)
	{
		auto temp = split_s(s[i]);
		int s0 = strInt(temp[0]);
		int s1 = strInt(temp[1]);
		int s2 = strInt(temp[2]);
		int s3 = strInt(temp[3]);
		string t0 = Char(LeftShift(s0) ^ LeftShift(s1) ^ s1 ^ s2 ^ s3);
		if (t0.length() < 2)
			t0 = "0" + t0;
		string t1 = Char(s0 ^ LeftShift(s1) ^ LeftShift(s2) ^ s2 ^ s3);
		if (t1.length() < 2)
			t1 = "0" + t1;
		string t2 = Char(s0 ^ s1 ^ LeftShift(s2) ^ s3 ^ LeftShift(s3));
		if (t2.length() < 2)
			t2 = "0" + t2;
		string t3 = Char(s0 ^ LeftShift(s0) ^ s1 ^ s2 ^ LeftShift(s3));
		if (t3.length() < 2)
			t3 = "0" + t3;
		str[i] = t0+t1+t2+t3;
	}
	return str;
}

string aes(string& plaintext, string& key)
{
	vector<string> keys = KeyExtend(key);
	int index = 0;
	vector<string> texts = MakeGroup(plaintext);
	for (int i = 0; i < 4; ++i)
		texts[i] = strXor(texts[i], keys[i]);
	index += 4;
	for (int k = 0; k < 10; ++k)
	{
		for (int j = 0; j < 4; ++j)
		{
			int len = texts[j].length();
			for (int i = 0; i < len; i += 2)
			{
				int x = Int(texts[j][i]);
				int y = Int(texts[j][i + 1]);
				string temp = Char(S[x][y]);
				if (temp.length() < 2)
					temp = "0" + temp;
				texts[j][i] = temp[0];
				texts[j][i + 1] = temp[1];
			}
		}
		texts = RowMove(texts);
		if (k < 9)
			texts = ColConfuse(texts);
		for (int i = 0; i < 4; ++i)
		{
			texts[i] = strXor(texts[i], keys[i + index]);
		}
		index += 4;
	}
	string ans = "";
	for (int i = 0; i < 4; ++i)
	{
		ans += texts[i];
	}
	return ans;
}

string Trans(string s)//将学号转为128bit16进制
{
	string str = "";
	for (char ch : s)
	{
		int num = ch;
		char s1 = num / 16 + 48;
		char s2 = num % 16 + 48;
		str += s1;
		str += s2;
	}
	while (str.length() < 32)
		str += "0";
	return str;
}


int main()
{
	string s="encryption!";
	
	string plaintext = Trans(s);
	string key = Trans(s);
	string ciphertext;
	auto t1 = chrono::high_resolution_clock::now();
	for (int i = 0; i < 10000; i++)
		ciphertext=aes(plaintext, key);
	auto t2 = chrono::high_resolution_clock::now();
	auto t3 = chrono::duration_cast<chrono::milliseconds>(t2 - t1);
	//因为一次加密时间接近0，所以直接加密10000次算平均值
	cout << "明文：" << plaintext << endl;
	cout << "密钥：" << key << endl;
	cout << "密文：" << ciphertext;
	cout << "10000次加密所用时间: " << t3.count() << "ms\n";
	cout << "平均每次加密所用时间: " << t3.count() / double(1000000) << "ms\n";
	

	return 0;
}
