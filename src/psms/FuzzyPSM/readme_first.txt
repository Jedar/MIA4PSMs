1)输入文件要求：

基础字典(DictFile): count+'\t'+pw （比如：basic_dic.txt）

训练字典(TrainFile): count+'\t'+pw （比如：train_dic.txt）

测试文件(TestFile): count+'\t'+pw （比如：test_set.txt）

需要强调的是，base_dic需要与test_set的来自同一语言，且basic_dic为较弱、较大（最好大于100万）的口令集，比如中文为Tianya, 英文为Rockyou。train_dic需要与test_set越接近越好，即语言相同，password policy相同，且网站类型最好比较接近，比如都同是来自社交网站。

三个输入文件的内容形如下：
391	123456
276	a123456
161	5201314
158	123456a
154	111111
133	woaini1314
98	123123
.......
即，每一行形如"频数(为整数)\t口令(为字符串)"。





2)输出文件：

得分文件(ScoreFile): pw+'\t'+psmScore (比如：PSM_result.txt)



3)具体运行方式：

1.Linux下编译源码 g++ fuzzypcfg_all_pw.cpp -o fuzzypcfg_all_pw

2.运行格式：
./fuzzypcfg_pw DictFile TrainFile TestFile ScoreFile

3.测试用例：
./fuzzypcfg_pw data/basic_dic.txt data/train_dic.txt data/test_set.txt data/PSM_result.txt

4.运行结果：
测试集的PSM得分会输出到得分文件中，格式为 pw+'\t'+strength，具体可见data目录下的输出文件

5.若直接使用run.sh脚本，可统计程序运行效率
./run.sh
终端输出如下信息：
运行时间(ms)11 
测试口令(个):1000000
每秒可测试口令数(个/s):90909

 
===============If you are not good at Chinese, please read the introduction below==========================

1. The "files" folder should initially contain at least three txt files: the base dictionary file (base_dic.txt in the example), the training file (train_dic.txt in the example), and the test file (test_set.txt in the example).

What should be emphasized are that: (1) "base_dic" is a large (e.g., with size larger than 1 million) and weak password set; (2) It needs to be from the same language as "test_set". For example, the 31.7 million Tianya dataset can be chosen as the Chinese base_dic, while the 32.6 million Rockyou  dataset can be chosen as the English base_dic,

And "train_dic" needs to be as close as possible to the "test_set", i.e., the same language and the same password policy. Moreover, it's better that the website types are similar, for example, both of them come from social network sites.

Following is the example of contents of the three input files:
391	123456
276	a123456
161	5201314
158	123456a
154	111111
133	woaini1314
98	123123
.......
i.e.,each line looks like "frequency(integer)\tpassword(string)".

2. see the additional file "linux_run.rtf".