module attributes {circt.loweringOptions = "locationInfoStyle=wrapInAtSquareBracket,omitVersionComment"} {
    hw.module @simple_structural(%a: i16 loc(unknown), %b: i16 loc(unknown), %c: i16 loc(unknown), %CLK: i1 loc(unknown)) -> (y: i16 loc(unknown), z: i16 loc(unknown)) {
        %1 = sv.reg name "a_reg" : !hw.inout<i16>
        loc("file.py":100:0)
        sv.alwaysff(posedge %CLK) {
            sv.passign %1, %a : i16
            loc("file.py":100:0)
        }
        loc("file.py":100:0)
        %2 = hw.constant 0 : i16
        loc("file.py":100:0)
        sv.initial {
            sv.bpassign %1, %2 : i16
            loc("file.py":100:0)
        }
        loc("file.py":100:0)
        %0 = sv.read_inout %1 : !hw.inout<i16>
        loc("file.py":100:0)
        %3 = comb.and %0, %c : i16
        loc("file.py":101:0)
        %4 = comb.or %0, %b : i16
        loc("file.py":102:0)
        hw.output %3, %4 : i16, i16
        loc(unknown)
    }
    loc("file.py":100:0)
}
loc(unknown)
