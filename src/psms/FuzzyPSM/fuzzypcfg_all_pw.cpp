#include<iostream>
#include<fstream>
#include<queue>
#include<time.h>
#include<algorithm>
#include<iomanip>
#include<math.h>
#include<cstring>
using namespace std;

#include "Trie.h"

//#define MIN3(a, b, c) ((a) < (b) ? ((a) < (c) ? (a) : (c)) : ((b) < (c) ? (b) : (c)))
//#define FILE_DICT "F://testdic.txt"	//字典文件的路径
//#define FILE_TRAINING "F://testtrain.txt"

#define MAX_LINE_LENGTH 128	//一行最大长度

//string filedictionary[3] = {"F://BaiduYunDownload//csdn_频数统计.txt",
//	"F://BaiduYunDownload//yahoo_频数统计.txt",
//	"F://BaiduYunDownload//tianya_频数统计.txt"};
char trainword[MAX_WORD_LENGTH];
char scoreword[MAX_WORD_LENGTH];

//三个规则，Concatenation,Leet,Misspelling 各自的count
double con = 0; double leet = 0;double mis = 0;double ins = 0;double sd = 0;double qd = 0;

double scorecon = 0;double scoreleet = 0;double scoreins = 0;double scoresd = 0;double scoreqd = 0;

double wordcnt = 0;double digitcnt = 0;double chcnt = 0;double spcnt = 0;

//规则各自对应的临时变量
double tmpcon = 0;double tmpleet = 0;double tmpmis = 0;double tmpins = 0;double tmpsd = 0;double tmpqd = 0;

//训练完后三个规则的概率
double pcon = 0;double pleet = 0;double pmis = 0;double pins = 0;double psd = 0;double pqd = 0;

//四个component各自的总count
double L = 0;double D = 0;double S = 0;double C = 0;

//四个component各自的最小count
double minL = 0;double minD = 0;double minS = 0;double minC = 0;

Trie<char> *DictTree = new Trie<char>();	//存储词典内容的Trie树
Trie<char> *LetterTree = new Trie<char>();	//存储单词的Trie树
Trie<char> *DigitTree = new Trie<char>();	//存储数字的Trie树
Trie<char> *SpecialTree = new Trie<char>();	//存储特殊字符的Trie树
Trie<char> *CharacterTree = new Trie<char>();	//存储非单词的letters的Trie树

struct tmptable		//用于临时存放将要插入树中的各项
{
	char str[MAX_WORD_LENGTH][MAX_WORD_LENGTH];
	int length;
};
tmptable LetterTable;
tmptable DigitTable;
tmptable SpecialTable;
tmptable CharacterTable;

//leet对应规则
char leetsrc[6] = {'@','3','0','$','1','7'};	//数字或特殊字符等
char leetdes[6] = {'a','e','o','s','i','t'};	//字母

/*int ed(char *s1, char *s2) {
    int x, y, s1len, s2len;
    s1len = strlen(s1);
    s2len = strlen(s2);
    int matrix[s2len+1][s1len+1];
    matrix[0][0] = 0;
    for (x = 1; x <= s2len; x++)
        matrix[x][0] = matrix[x-1][0] + 1;
    for (y = 1; y <= s1len; y++)
        matrix[0][y] = matrix[0][y-1] + 1;
    for (x = 1; x <= s2len; x++)
        for (y = 1; y <= s1len; y++)
            matrix[x][y] = MIN3(matrix[x-1][y] + 1, matrix[x][y-1] + 1, matrix[x-1][y-1] + (s1[y-1] == s2[x-1] ? 0 : 1));

    return(matrix[s2len][s1len]);
}*/
void clear()
{
	LetterTable.length = 0;
	DigitTable.length = 0;
	SpecialTable.length = 0;
	CharacterTable.length = 0;
	tmpcon = 0;tmpleet = 0;//tmpmis = 0;tmpins = 0;
}
bool isDigit(char ch)
{
	return ch >= '0' && ch <= '9';
}
bool isAlpha(char ch)
{
	return (ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z');
}
void lowercase(char *word)		//将大写字母转化为小写
{
	int len = strlen(word);
	for (int i = 0;i < len;i++)
	{
		if (word[i] >= 'A' && word[i] <= 'Z')
			word[i] = word[i] - 'A' + 'a';
	}
}

void CreateDictTree(char *FILE_DICT)		//构建词典的Trie树
{

	ifstream filedict;
	filedict.open(FILE_DICT);
	if (!filedict)
		cout << "filedict error" << endl;

	int ln = 0;
	char password[1000];
	int count = 0;
	while (!filedict.eof())
	{
		ln++;

		//	break;
		//if (ln == 10975060)
		//	cout << ln << endl;
		//	continue;
		//if (ln > 19705060 && ln%100000 ==0)
		//	cout << ln << endl;
		filedict >> count;
		filedict.getline(password,1000);
		int l = strlen(password);

		if (l <= 3|| l > 30)//忽略长度小于3的密码
		{
			//cout << ln << " <3 " << password << endl;
			continue;
		}
		for (int i = 0;i < l;i++)
			password[i] = password[i+1];
		password[l] = '\0';
		l--;

		strcpy(trainword,password);

		l = strlen(trainword);
		lowercase(trainword);
		//strcpy(dict[dictidx],trainword);
		//dictidx++;
		DictTree->insert(trainword,l,count);	//将单词插入Trie树中
	}
	filedict.close();

}

bool allmatch(char *word)
{
	char result[MAX_WORD_LENGTH];

	int len = strlen(word);
	int start = 0;
	int end = 0;
	while(1)
	{
		result[0] = '\0';
		end = DictTree->match(word,result,len,start);
		if (end == start)
		{
			LetterTable.length = 0;	//匹配失败，LetterTable清空
			tmpcon = 0;
			return false;
		}
		else
		{
			int idx = LetterTable.length;			//可能插入单词树中，放入临时表中
			strcpy(LetterTable.str[idx],result);
			LetterTable.length++;
		}
		start = end;
		if (start == len)
			break;
		tmpcon++;///////////////////con规则+1
	}
	return true;
}

bool useleet(char *pw)
{

	int len = strlen(pw);
	int flag = 0;
	for (int i = 0;i < len;i++)
	{
		for (int j = 0;j < 6;j++)
		{
			if (pw[i] == leetsrc[j])
			{
				flag = 1;
				break;
			}
		}
		if (flag == 1)
			break;
	}
	if (flag == 0)
		return false;
	//如果pw中没有出现leet的字符，就直接返回false

	char tmppw[MAX_WORD_LENGTH];
	strcpy(tmppw,pw);

	for (int i = 0;i <= len;i++)
	{
		for (int j = 0;j < 6;j++)
		{
			if (leetsrc[j] == tmppw[i])
			{
				tmppw[i] = leetdes[j];
				tmpleet++;
				break;
			}
		}
	}
	return allmatch(tmppw);

}

/*bool usemis(char *pw)
{
	int tmpidx = -1;
	int mined = 3;
	for (int i = 0;i < dictidx;i++)
	{
		int tmped = ed(dict[i],pw);
		if (tmped > 1)
			continue;
		else
		{
			if (tmped < mined)
			{
				mined = tmped;
				tmpidx = i;
			}
			if (tmped == 1)
				break;
		}
	}
	if (tmpidx == -1)
		return false;
	//allmatch(dict[tmpidx]);
	tmpmis++;
	return true;
}*/
bool usesd(char *pw)
{
	char c = pw[0];
	if (c >= 'A' && c <= 'Z')
		return true;
	return false;
}

bool useqd(char *pw)
{
	int flag = 0;
	int len = strlen(pw);
	for (int i = 0;i < len;i++)
	{
		char c = pw[i];
		if (!isAlpha(c))
			continue;
		else
			flag = 1;
		if (c <'A' || c > 'Z')
			return false;
	}
	if (flag)
		return true;
	return false;
}

bool useins(char *pw)
{
	int len = strlen(pw);
	int j = 0;
	char tmppw[MAX_WORD_LENGTH];
	int flag1 = 0;
	int flag2 = 0;
	int flag3 = 0;
	for (int i = 0;i < len;i++)
	{
		char c = pw[i];
		if (isAlpha(c))
		{
			tmppw[j++] = c;
			flag1 = 1;
			if (flag2)
				flag3 = 1;
		}
		else
		{
			if (flag1)
				flag2 = 1;
		}
	}
	tmppw[j] = '\0';
	if (flag3)
		return allmatch(tmppw);
	return false;
}
void parse(char *pw)	//输入密码pw，分析这个密码采用了什么规则以及有哪些components
{
	bool flag;
	flag = allmatch(pw);
	if (flag == true)
		return;
	else
		clear();
	/*//insert
	flag = useins(pw);
	if (flag == true)
	{
		tmpins++;
		return;
	}
	else
		clear();*/
	//leet
	flag = useleet(pw);
	if (flag == true)
		return;
	else
		clear();
/*	//misspelling
	flag = usemis(pw);
	if (flag == true)
		return;
	else
		clear();*/

	char result[MAX_WORD_LENGTH];

	int len = strlen(pw);
	int start_ = 0;
	int end_ = 0;
	char tmpword[MAX_WORD_LENGTH];
	while(1)
	{
		result[0] = '\0';
		end_ = DictTree->match(pw,result,len,start_);
		if (end_ == start_)
		{

			for (int i = start_;i < len;i++)
				tmpword[i-start_] = pw[i];
			tmpword[len-start_] = '\0';
			break;
		}
		else
		{
			int idx = LetterTable.length;			//可能插入单词树中，放入临时表中
			strcpy(LetterTable.str[idx],result);
			LetterTable.length++;
		}
		start_ = end_;
		if (start_ == len)
			break;
		tmpcon++;///////////////////con规则+1
	}
	//上面都不满足，拆分，调用parseletter()
	//0:letter	1:digit		2:special
	int start[3] = {0,0,0};
	int end[3] = {0,0,0};
	int cur;
	int nextcur;

	len = strlen(tmpword);
	if (isAlpha(tmpword[0]))
	{
		cur = 0;
		end[0] = 1;
	}
	else if (isDigit(tmpword[0]))
	{
		cur = 1;
		end[1] = 1;
	}
	else
	{
		cur = 2;
		end[2] = 1;
	}
	for (int i = 1;i < len;i++)
	{
		if (isAlpha(tmpword[i]))
		{
			if (cur == 0)
				continue;
			else
			{
				end[cur] = i;
				nextcur = 0;
				start[0] = i;
			}
		}
		else if (isDigit(tmpword[i]))
		{
			if (cur == 1)
				continue;
			else
			{
				end[cur] = i;
				nextcur = 1;
				start[1] = i;
			}
		}
		else
		{
			if (cur == 2)
				continue;
			else
			{
				end[cur] = i;
				nextcur = 2;
				start[2] = i;
			}
		}
		tmpcon++;
		int j;
		if (cur == 0)
		{
			int idx = CharacterTable.length;
			for (j = 0;j < end[cur]-start[cur];j++)
			{
				CharacterTable.str[idx][j] = tmpword[j+start[cur]];
			}
			CharacterTable.str[idx][j] = '\0';
			CharacterTable.length++;
		}
		if (cur == 1)
		{
			int idx = DigitTable.length;
			for (j = 0;j < end[cur]-start[cur];j++)
			{
				DigitTable.str[idx][j] = tmpword[j+start[cur]];
			}
			DigitTable.str[idx][j] = '\0';
			DigitTable.length++;
		}
		if (cur == 2)
		{
			int idx = SpecialTable.length;
			for (j = 0;j < end[cur]-start[cur];j++)
			{
				SpecialTable.str[idx][j] = tmpword[j+start[cur]];
			}
			SpecialTable.str[idx][j] = '\0';
			SpecialTable.length++;
		}
		cur = nextcur;
	}
	end[cur] = len;
	int j;
	if (cur == 0)
	{
		int idx = CharacterTable.length;
		for (j = 0;j < end[cur]-start[cur];j++)
		{
			CharacterTable.str[idx][j] = tmpword[j+start[cur]];
		}
		if (j != MAX_WORD_LENGTH)
			CharacterTable.str[idx][j] = '\0';
		CharacterTable.length++;
	}
	if (cur == 1)
	{
		int idx = DigitTable.length;
		for (j = 0;j < end[cur]-start[cur];j++)
		{
			DigitTable.str[idx][j] = tmpword[j+start[cur]];
		}
		if (j != MAX_WORD_LENGTH)
			DigitTable.str[idx][j] = '\0';
		DigitTable.length++;
	}
	if (cur == 2)
	{
		int idx = SpecialTable.length;
		for (j = 0;j < end[cur]-start[cur];j++)
		{
			SpecialTable.str[idx][j] = tmpword[j+start[cur]];
		}
		if (j != MAX_WORD_LENGTH)
			SpecialTable.str[idx][j] = '\0';
		SpecialTable.length++;
	}

}
int main(int argc, char *argv[])
{
    if (argc != 5)
    {
        exit(1);
    }
	char *FILE_TRAINING = argv[2];
	// "/Volumes/外置硬盘/密码库处理/统计/密码长度最大30/dodonew_频数统计.txt"	//训练文件的路径
	//#define FILE_SCORING "F://phpbb_频数统计.txt"		//评分文件的路径
    char *FILE_TEST = argv[3];
	char *FILE_OUT = argv[4];
	// "./score_cn3_fuzzypcfg.txt" //输出评分
	char *FILE_DICT = argv[1];
	// "/Volumes/外置硬盘/密码库处理/统计/密码长度最大30/tianya_频数统计.txt"	//字典文件的路径


	CreateDictTree(FILE_DICT);	//构建词典的Trie树
	//cout << "建立字典树完成" << endl;
	//然后训练，对读入的每个password进行处理

	ifstream filetraining;
	filetraining.open(FILE_TRAINING);
	if (!filetraining)
		cout << "filetraining error" << endl;

	int count = 0;
	char password[50];
	int totalcount = 0;
	int ln = 0;
	while (!filetraining.eof())
	{
		clear();
		tmpsd = 0;
		tmpqd = 0;
		ln++;
		if (ln%10000 == 0)
		{
			//cout << ln << endl;
			// cout << password << endl;
		}


		//if (ln>13676000)
		//	cout << ln;
		filetraining >> count;
		filetraining.getline(password,50);
		totalcount += count;
		int l = strlen(password);
		if (l > 30)	//忽略长度超过30的密码
			continue;
		for (int i = 0;i < l;i++)
			password[i] = password[i+1];
		password[l] = '\0';
		l--;
		//if (ln>13676000)
		//	cout << "   1";
		strcpy(trainword,password);
		if (usesd(trainword))
			tmpsd ++;
		if (useqd(trainword))
			tmpqd ++;
		lowercase(trainword);
		int len = strlen(trainword);
		//if (ln>13676000)
		//	cout << "   2";
		//上面读入密码，下面分析其规则和components


		parse(trainword);
		//然后对应规则count增加，components插入对应树中。
		//if (ln>13676000)
		//	cout << "   3";
		con  += tmpcon*count;
		leet += tmpleet*count;
		//mis += tmpmis*count;
		sd += tmpsd*count;
		qd += tmpqd*count;
		//ins += tmpins*count;
		//if (ln>13676000)
		//	cout << "   4";
		for (int i = 0;i < LetterTable.length;i++)
		{
			LetterTree->insert(LetterTable.str[i],strlen(LetterTable.str[i]),count);
		}
		L += LetterTable.length*count;
		//if (ln>13676000)
		//	cout << "   5  ";

		for (int i = 0;i < DigitTable.length;i++)
		{
		//	if (ln>13676000)
		//		cout << DigitTable.str[i]  << "   " << count;
			DigitTree->insert(DigitTable.str[i],strlen(DigitTable.str[i]),count);
		}

		D += DigitTable.length*count;
		//if (ln>13676000)
		//	cout << "   6";
		for (int i = 0;i < SpecialTable.length;i++)
		{
			SpecialTree->insert(SpecialTable.str[i],strlen(SpecialTable.str[i]),count);
		}
		S += SpecialTable.length*count;
		//if (ln>13676000)
		//	cout << "   7";
		for (int i = 0;i < CharacterTable.length;i++)
		{
			CharacterTree->insert(CharacterTable.str[i],strlen(CharacterTable.str[i]),count);
		}
		C += CharacterTable.length*count;
		//if (ln>13676000)
		//	cout <<"   8" <<  endl;
	}
	//cout << "--------------------" << endl;
	//cout << ln << endl;
	pcon = con/totalcount;
	pleet = leet/totalcount;
	//pmis = mis/totalcount;
	psd = sd/totalcount;
	pqd = qd/totalcount;
	//pins = ins/totalcount;


	//cout << "con:	" << con << endl;
	//cout << "leet:	" << leet << endl;
	//cout << "mis:	" << mis << endl;
	//cout << "sd:	" << sd << endl;
	//cout << "qd:	" << qd << endl;
	//cout << "ins:	" << ins << endl;
	//cout << "totalcount:	" << totalcount << endl;

	//minL,minD,minS,minC，（应遍历四个树来查找最小count）暂时假设都为1
	minL = 1; minD = 1; minS = 1; minC = 1;

	ifstream filescoring;
	filescoring.open(FILE_TEST);
	if (!filescoring)
		cout << "filescoring error" << endl;
	ofstream fileout;
	fileout.open(FILE_OUT);
	if (!fileout)
		cout << "fileout error" << endl;
	ln = 0;
	totalcount = 0;
	double weakhit = 0;
	double stronghit = 0;
	double weakcount = 0;
	double strongcount = 0;
	while (true)
	{
		clear();
		tmpsd = 0;
		tmpqd = 0;


		filescoring >> count;
		filescoring.getline(password,1000);
		if (filescoring.eof())
		{
			break;
		}
		/*if (count < 500 && count > 1)
			continue;
		if (count >= 500)
			weakcount++;
		if (count == 1)
			strongcount++;*/
		//totalcount += count;
		int l = strlen(password);
		ln++;
		double score = 1;	//score为密码的评分
		if (l > 30)	//忽略长度超过30的密码
			score = 0;
		else
		{
			//if (ln > 100000)
			//	break;
			for (int i = 0;i < l;i++)
				password[i] = password[i+1];
			password[l] = '\0';
			l--;
			strcpy(scoreword,password);
			if (usesd(scoreword))
				tmpsd ++;
			if (useqd(scoreword))
				tmpqd ++;
			lowercase(scoreword);
			int len = strlen(scoreword);
			parse(scoreword);

			scorecon += tmpcon * count;
			scoreleet += tmpleet*count;
			//scoremiss += tmpmis*count;
			scoresd += tmpsd*count;
			scoreqd += tmpqd*count;
			//scoreins += tmpins*count;

			wordcnt += LetterTable.length*count;
			digitcnt += DigitTable.length*count;
			chcnt += CharacterTable.length*count;
			spcnt += SpecialTable.length*count;

			//计算score。score=各个components及rules的概率乘积，再取log
			for (int i = 0;i < tmpcon;i++)
				score *= pcon;
			for (int i = 0;i < tmpleet;i++)
				score *= pleet;
			//for (int i = 0;i < tmpmis;i++)
			//	score *= pmis;
			for (int i = 0;i < tmpsd;i++)
				score *= psd;
			for (int i = 0;i < tmpqd;i++)
				score *= pqd;
			//for (int i = 0;i < tmpins;i++)
			//	score *= pins;

			for (int i = 0;i < LetterTable.length;i++)
			{
				int p = LetterTree->find(LetterTable.str[i],strlen(LetterTable.str[i]));
				if (p == 0)
					p = minL;
				score *= p/L;
			}
			for (int i = 0;i < DigitTable.length;i++)
			{
				int p = DigitTree->find(DigitTable.str[i],strlen(DigitTable.str[i]));
				if (p == 0)
					p = minD;
				score *= p/D;
			}
			for (int i = 0;i < SpecialTable.length;i++)
			{
				int p = SpecialTree->find(SpecialTable.str[i],strlen(SpecialTable.str[i]));
				if (p == 0)
					p = minS;
				score *= p/S;
			}
			for (int i = 0;i < CharacterTable.length;i++)
			{
				int p = CharacterTree->find(CharacterTable.str[i],strlen(CharacterTable.str[i]));
				if (p == 0)
					p = minC;
				score *= p/C;
			}
			//if (count >= 500 && score < 15)
			//	weakhit++;
			//if (count == 1 && score > 15)
			//	stronghit++;
	        if (isnan(score))
	        {
	            cout<<password<<endl;
	        }
		}
		

        fileout <<password<<"\t"<< setiosflags(ios::scientific) << score << endl; //评分输出到文件中
	}
	/*
	cout << "平均每个密码中的单词组件：" << wordcnt/totalcount << endl;
	cout << "平均每个密码中的数字组件：" << digitcnt/totalcount << endl;
	cout << "平均每个密码中的character组件：" << chcnt/totalcount << endl;
	cout << "平均每个密码中的特殊字符组件：" << spcnt/totalcount << endl;
	cout << "-------------------" << endl;
	cout << "totalcount:" << totalcount << endl;
	cout << scorecon << " 平均每个密码中的连接规则：" << scorecon/totalcount << endl;
	cout << scoreleet << " 平均每个密码中的leet规则：" << scoreleet/totalcount << endl;
	//cout << scoremiss << " 平均每个密码中的miss规则：" << scoremiss/totalcount << endl;
	cout << scoresd << " 平均每个密码中的sd规则：" << scoresd/totalcount << endl;
	cout << scoreqd << " 平均每个密码中的qd规则：" << scoreqd/totalcount << endl;
	//cout << scoreins << " 平均每个密码中的ins规则：" << scoreins/totalcount << endl;
	*/
	//cout << stronghit/strongcount << endl;
	//cout << weakhit/weakcount << endl;
	return 0;
}
