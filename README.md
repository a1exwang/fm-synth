# fm-synth
Image-Line Sytrus-like FM Synthesizer Implementation in Python.

### TODOs

#### 功能性TODOs


- Oscillator
    - 单周期波形更多样化, 甚至可以手动绘制, 或者给函数表达式
    - 实现 ADSR, attack-decay-sustain-release,
        - 所有的 Operator 需要添加调幅输入(现在只有 Oscillator 支持调幅)
        - 如何得知一个按键按下

- Filter
    - 换用 IIR 滤波器, 提升性能 


#### 易用性TODOs

1. 用 pyqt 搭起 GUI 框架, 把现有的 Oscilloscope 放进去, Operator 的参数用滑动条调节

#### 模型

1. 
