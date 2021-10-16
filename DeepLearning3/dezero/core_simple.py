import weakref
import numpy as np
import contextlib

# =============================================================================
# Config
# =============================================================================
class Config:
    enable_backprop = True


@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad():
    return using_config('enable_backprop', False)

# =============================================================================
# Variable / Function
# =============================================================================
# DeZeroで使用する変数クラス
class Variable:
    def __init__(self, data, name =None):
        # dataがndarray以外だったらエラーが出るようにする
        if data is not None:
            if not isinstance(data,np.ndarray):
                raise TypeError('{} is not suppported'.format(type(data)))
        self.data = data  #　通常の値
        self.name=name
        self.grad=None    #　dataに対応した微分値
        self.creator=None #このクラスの変数が生成される関数　例：y=f(x)のとき　yにとってfがcreator
        self.generation=0 # どの世代に属するか

    # creatorのsetter
    def set_creator(self,func):
        self.creator=func
        self.generation=func.generation+1 #生成されるVariableはcreaterよりも１つ高い世代になる

    # 逆伝播を行う関数(ループを使った実装)
    def backward(self,retain_grad=False):
        # gradがNoneの場合、自動で微分を生成する
        # ones_like：既存の配列と同じシェイプで，すべての要素の値が 1 の配列を生成
        if self.grad is None:
            self.grad=np.ones_like(self.data)

        funcs=[]
        seen_set=set()
        # DeZeroの関数を登録するときに使用
        # 世代の値順に並び替えられる
        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x: x.generation)
        
        add_func(self.creator)
        while funcs:
            f=funcs.pop() # 関数を取得
            # gys=[output.grad for output in f.outputs] # 出力変数がタプルで保存されているのでリストにまとめる
            gys=[output().grad for output in f.outputs] #Functionクラスで修正したのでこっちも修正
            gxs=f.backward(*gys) # リストを展開して関数fの逆伝播を呼び出す
            if not isinstance(gxs,tuple):
                gxs=(gxs,)
            # 伝播する微分値をVariableのインスタンス変数gradに設定する
            # zip()は複数のイテラブルオブジェクト（リストやタプルなど）の要素をまとめる関数
            for x,gx in zip(f.inputs, gxs):
                if x.grad is None:
                    x.grad=gx
                else:
                    x.grad+=gx
                # 関数fの入力のうち別の関数から生成された変数があれば微分値を計算する必要があるのでstackに追加する
                # backpropは深さ優先
                if x.creator is not None:
                    add_func(x.creator) # 1つ目の関数をリストに追加
            # 微分を消去するモード
            if not retain_grad:
                for y in f.outputs:
                    y().grad=None #yはweakref
    # 微分をリセットする
    def cleargrad(self):
        self.grad=None
    
    #インスタンス変数としてデータサイズにアクセス
    @property
    def shape(self):
        return self.data.shape

    #インスタンス変数としてデータ次元数にアクセス
    @property
    def ndim(self):
        return self.data.ndim

    #インスタンス変数として要素数にアクセス
    @property
    def size(self):
        return self.data.size

    #インスタンス変数としてデータ型にアクセス
    @property
    def dtype(self):
        return self.data.dtype
    
    #   インスタンスに対してlen関数実行
    def __len__(self):
        return len(self.data)
    
    # ndarrayインスタンスの内容を出力する
    def __repr__(self):
        if self.data is None:
            return 'variable(None)'
        p=str(self.data).replace('¥n','¥n'+' '*9)
        return 'valiable('+p+')'
    
    # # 掛け算メソッドのオーバーロード
    # def __mul__(self,other):
    #     return mul(self,other)
    # # 足し算メソッドのオーバーロード
    # def __add__(self,other):
    #     return add(self,other)  


#  Variableクラスを処理する関数を定義するクラス
# このクラスを基底クラスとして、共通する機能を実現
class Function:
    # *を変数につけることで可変長引数にする
    def __call__(self, *inputs):
        # ndarrayが入力されてもVariableインスタンスとして扱える
        inputs = [as_variable(x) for x in inputs]

        xs = [x.data for x in inputs]  #　データを取り出す
        ys = self.forward(*xs) #　実際の計算
        # 複数の値の入力に対応
        if not isinstance(ys,tuple):
            ys=(ys,)
        outputs = [Variable(as_array(y)) for y in ys]# Variableとして返す
        
        # 逆伝播有効
        if Config.enable_backprop:
            
            self.generation=max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self) # 出力変数に生みの親を覚えさせる
            self.inputs=inputs #　入力された変数を覚える
            self.outputs=[weakref.ref(output) for x in outputs] #　出力も覚えさせる

        #リストの要素が1つの時は最初の要素を返す
        return outputs if len(outputs) > 1 else outputs[0]

    #順伝播を行う機能
    def forward(self,x):
        raise NotImplementedError() #意図的に例外を発生させる
    # 微分の罫線を行う逆伝播の機能
    def backward(self,gy):
        raise NotImplementedError()

# =============================================================================
# 四則演算 / 演算子のオーバーロード
# =============================================================================

# 掛け算を行うクラス
class Mul(Function):
    def forward(self, x0, x1):
        y = x0 * x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return gy * x1, gy * x0

# 掛け算を行うクラス
class Add(Function):
    def forward(self, x0, x1):
        y = x0 + x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return gy + x1, gy + x0

def mul(x0, x1):
    x1 = as_array(x1)
    return Mul()(x0, x1)


# 足し算を行うクラス
class Add(Function):
    def forward(self, x0,x1):
        y=x0+x1
        return y
    def backward(self, gy):
        return gy,gy
#function classを継承して利便性向上
class Square(Function):
    def forward(self, x):
        return x**2
    #y=x^2の微分を計算dy/dx=2x
    def backward(self,gy):
        x=self.inputs[0].data
        gx=2 * x * gy
        return gx

class Exp(Function):
    def forward(self, x):
        y=np.exp(x)
        return y
    def backward(self,gy):
        x=self.input.data
        gx=np.exp(x)*gy
        return gx

def square(x):
    f=Square()
    return f(x)
def exp(x):
    f=Exp()
    return f(x)

def add(x0,x1):
     x1 = as_array(x1)
     return Add()(x0, x1)

def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x

# インスタンスの変換
def as_variable(obj):
    if isinstance(obj, Variable):
        return obj
    return Variable(obj)

# 負の数の微分
class Neg(Function):
    def forward(self, x):
        return -x

    def backward(self, gy):
        return -gy

def neg(x):
    return Neg()(x)

# 引き算
class Sub(Function):
    def forward(self, x0, x1):
        y = x0 - x1
        return y

    def backward(self, gy):
        return gy, -gy


def sub(x0, x1):
    x1 = as_array(x1)
    return Sub()(x0, x1)


def rsub(x0, x1):
    x1 = as_array(x1)
    return sub(x1, x0) # x1, x0を入れ替え

# 割り算
class Div(Function):
    def forward(self, x0, x1):
        y = x0 / x1
        return y

    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        gx0 = gy / x1
        gx1 = gy * (-x0 / x1 ** 2)
        return gx0, gx1


def div(x0, x1):
    x1 = as_array(x1)
    return Div()(x0, x1)


def rdiv(x0, x1):
    x1 = as_array(x1)
    return div(x1, x0)

# 累乗
class Pow(Function):
    def __init__(self, c):
        self.c = c

    def forward(self, x):
        y = x ** self.c
        return y

    def backward(self, gy):
        x = self.inputs[0].data
        c = self.c

        gx = c * x ** (c - 1) * gy
        return gx


def pow(x, c):
    return Pow(c)(x)

# Variableクラスの特殊メソッド定義
def setup_variable():
    Variable.__add__ = add
    Variable.__radd__ = add
    Variable.__mul__ = mul
    Variable.__rmul__ = mul
    Variable.__neg__ = neg
    Variable.__sub__ = sub
    Variable.__rsub__ = rsub
    Variable.__truediv__ = div
    Variable.__rtruediv__ = rdiv
    Variable.__pow__ = pow