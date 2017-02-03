# fm-synth
Image-Line Sytrus-like FM Synthesizer Implementation in Python.

### TODOs

#### 功能性TODOs


- Oscillator
    - Done. 单周期波形更多样化. \[Unimportant 手动绘制, 或者给函数表达式 ?\]
    - Done. 实现 ADSR, attack-decay-sustain-release,
        - Done. 所有的 Operator 需要添加调幅输入(现在只有 Oscillator 支持调幅)
        - Done. 如何得知一个按键按下(不需要了, 现在所有 Osc 有调幅和调频两个输入)
    
    - 支持左右声道(PAN).

- Filter
    - 换用 IIR 滤波器, 提升性能 
    - 支持 Sytrus 的滤波器那样既可以调节通带频率, 又可以调节衰减的 Filter


#### 易用性TODOs

1. Done. 用 pyqt 搭起 GUI 框架, 把现有的 Oscilloscope 放进去, Operator 的参数用滑动条调节

2. Done. 支持滑动条的 Channel, 每个 Operator 可以在全局注册一个名字唯一的 Channel, 一个滑动条可以通过选择 Channel 来选择该
    滑动条控制哪个 Operator 的参数.

#### 模型

1. 用 JSON 或者 YAML 来描述 Operator 之间的连接关系
