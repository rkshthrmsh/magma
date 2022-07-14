hw.module @test_when_nested_TupleBits2Bit(%I_0_0: i2, %I_0_1: i1, %I_1_0: i2, %I_1_1: i1, %S: i1) -> (O_0: i2, O_1: i1) {
    %2 = sv.reg {name = "O0_reg"} : !hw.inout<i2>
    %3 = sv.reg {name = "O1_reg"} : !hw.inout<i1>
    sv.alwayscomb {
        sv.bpassign %2, %I_1_0 : i2
        sv.bpassign %3, %I_1_1 : i1
        sv.if %S {
            sv.bpassign %2, %I_0_0 : i2
            sv.bpassign %3, %I_0_1 : i1
        }
    }
    %0 = sv.read_inout %2 : !hw.inout<i2>
    %1 = sv.read_inout %3 : !hw.inout<i1>
    hw.output %0, %1 : i2, i1
}
