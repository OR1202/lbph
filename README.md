正面画像からの顔の検出は，
試験中継続的に顔を検出することが可能であり，
かつ検出精度が高い
Viola and Jones\cite{detect}の提案した顔検出手法を用いた．
これは，あらかじめ重み付けをした大量の弱識別器を画像の局所（矩形）領域にあてはめ，識別器と合致すれば重みに-1を乗じたものを算出し，
これらの結果をすべて足し合わせた結果が0よりも大きければ顔とみなす方法である．
顔検出に失敗した場合，以降の顔認証処理は行われない．
ただし，本論文は顔向きが頻繁に変動するような試験形式を対象としていないため，
問題解答中一度も顔が検出できない状況はないものとしている．

顔画像の特徴は，
LBPH (Local Binary Patterns Histogram)とした．
LBPは注目画素とその近傍画素の大小比較によって特徴量が計算されるため計算コストが少なく，
登録画像撮影時とe-Testing受験時における撮影環境の違いが及ぼす
一様な照明変化の影響を受けづらいという利点がある．
また，LBPは生体特徴に対して特別な最適化が不要であるため，
極少数の登録画像からでも最低限の認証精度が得られる．
画像の任意の点$(x,y)$のLBPは以下の式で表される．

$$
	{\rm LBP}(x,y)=\sum_{p=0}^{\rm P-1}2^{p}{\rm T}\left({\rm V}(x_{p},y_{p})-{\rm V}(x,y)\right)\\
$$

$$
	x_{p}=x+{\rm R}\cos(2{\pi}p/\rm P)
$$

$$
	y_{p}=y-{\rm R}\sin(2{\pi}p/\rm P)
$$

${\rm V}(x,y)$は画像上の点$(x,y)$の輝度値を表す．
$\rm P$はあらかじめ設定した参照点の数であり，$x_p, y_p$は点$(x,y)$の周辺座標である．
$\rm R$は点$(x,y)$と参照点との距離を示す．
${\rm T}(a)$は，$a$が0より小さければ1，大きければ0を返すしきい値関数である．
各画素ごとにLBPを算出した後，画像内の領域を$d \times d$に分割し，
分割した領域ごとにuniform-patternの出現頻度を計測してLBPHとする．
各領域ごとのLBPHを連結し，連結したLBPHを顔特徴ベクトルとする．
特徴ベクトルの次元数は各パラメタに依存し，
特に$\rm P$によって指数的に増加する．
$\rm R$は処理する画像サイズにも依るが，
大きすぎると画像の局所特徴をとらえられなくなる．
$\rm d$は画像の空間情報の保持に関するパラメタであり，
小さければ顔姿勢の変動に頑健になるが空間特徴による識別が困難になり，
大きければ画像の状態を識別しやすくなる一方で位置の変動に影響を受けやすくなる．
本論文では計算量や認証精度の観点から
$\rm P = 8$，
$\rm R = 1$，
$\rm d = 8$
とした．


二つのLBPHの類似度は，
Ahonenらが検討した複数の類似度計算方法の内，認証精度が高く計算が単純である
$\chi^2$距離とした．
２つのLBPHを$\boldsymbol{R}$と$\boldsymbol{Q}$とする．
ただし，LBPHは頻度を相対度数に正規化して距離計算を行うものとする．
また，登録顔情報
が$N$件存在した場合は，
以下のように特徴量ベクトルの重心ベクトル$\boldsymbol{R}$を求め，
それをテンプレートとする．

$$
\boldsymbol{R}=\frac{1}{N}\sum_{n=1}^N\boldsymbol{R}_n
$$

この場合，$\boldsymbol{R}$と$\boldsymbol{Q}$の距離は式で求められる．
ただし，$r_i+q_i=0$の時の局所距離は0とした．

$$
\chi^2(\boldsymbol{R},\boldsymbol{Q}) = \sum_{i} \frac{(r_i-q_i)^2}{r_i+q_i}
$$

$\chi^2$距離は1問題につき複数算出されるが，
判定の際には問題の解答中に算出された距離を平均化し，
平均距離に-1を乗じた値をその問題における顔類似度$s_{\rm F}$とする．


## 参考文献
- P.Viola and M.Jones, ``Rapid object detection using a boosted cascade of simple features,'' Proc Of Computer Vision and Pattern Recognition, vol.1, pp.511-518, 2001. DOI: 10.1109/CVPR.2001.990517
- T.Ahonen, A.Hadid, and M.Pietikainen,  ``Face recognition with local binary patterns,'' Springer Verlag Berlin Heidelberg Lecture Notes in Computer Science, vol.3021, pp.469-481, 2004.