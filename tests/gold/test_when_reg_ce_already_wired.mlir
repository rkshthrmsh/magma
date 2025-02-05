module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @test_when_reg_ce_already_wired(%I: i8, %x: i1, %y: i1, %CLK: i1) -> (O: i8) {
        %2 = sv.reg : !hw.inout<i8>
        %1 = sv.read_inout %2 : !hw.inout<i8>
        sv.alwayscomb {
            sv.bpassign %2, %0 : i8
            sv.if %y {
                sv.bpassign %2, %I : i8
            }
        }
        %4 = sv.wire sym @test_when_reg_ce_already_wired._WHEN_ASSERT_0 name "_WHEN_ASSERT_0" : !hw.inout<i8>
        sv.assign %4, %1 : i8
        %3 = sv.read_inout %4 : !hw.inout<i8>
        %5 = sv.reg name "Register_inst0" : !hw.inout<i8>
        sv.alwaysff(posedge %CLK) {
            sv.if %x {
                sv.passign %5, %3 : i8
            }
        }
        %6 = hw.constant 0 : i8
        sv.initial {
            sv.bpassign %5, %6 : i8
        }
        %0 = sv.read_inout %5 : !hw.inout<i8>
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%y, %3, %I) : i1, i8, i8
        %8 = hw.constant -1 : i1
        %7 = comb.xor %8, %y : i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%7, %3, %0) : i1, i8, i8
        hw.output %0 : i8
    }
}
