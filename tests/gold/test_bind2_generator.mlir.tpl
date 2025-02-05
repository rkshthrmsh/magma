module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @LogicAsserts(%I: i1, %O: i1, %other: i1) -> () attributes {output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_generator_bind_files.list">} {
        sv.verbatim "{{0}} {{1}} {{2}}" (%I, %O, %other) : i1, i1, i1
    }
    hw.module @Logic(%I: i1) -> (O: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        hw.instance "LogicAsserts_inst0" sym @Logic.LogicAsserts_inst0 @LogicAsserts(I: %I: i1, O: %0: i1, other: %I: i1) -> () {doNotPrint = true}
        hw.output %0 : i1
    }
    sv.bind #hw.innerNameRef<@Logic::@Logic.LogicAsserts_inst0>
    hw.module @LogicAsserts_unq1(%I: i2, %O: i2, %other: i1) -> () attributes {output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_generator_bind_files.list">} {
        sv.verbatim "{{0}} {{1}} {{2}}" (%I, %O, %other) : i2, i2, i1
    }
    hw.module @Logic_unq1(%I: i2) -> (O: i2) {
        %1 = hw.constant -1 : i2
        %0 = comb.xor %1, %I : i2
        %2 = comb.extract %I from 0 : (i2) -> i1
        hw.instance "LogicAsserts_inst0" sym @Logic_unq1.LogicAsserts_inst0 @LogicAsserts_unq1(I: %I: i2, O: %0: i2, other: %2: i1) -> () {doNotPrint = true}
        hw.output %0 : i2
    }
    sv.bind #hw.innerNameRef<@Logic_unq1::@Logic_unq1.LogicAsserts_inst0>
    hw.module @Top(%I: i2) -> (O: i2) {
        %0 = comb.extract %I from 0 : (i2) -> i1
        %1 = hw.instance "Logic_inst0" @Logic(I: %0: i1) -> (O: i1)
        %2 = comb.extract %I from 1 : (i2) -> i1
        %3 = hw.instance "Logic_inst1" @Logic(I: %2: i1) -> (O: i1)
        %4 = comb.concat %3, %1 : i1, i1
        %5 = hw.instance "Logic_inst2" @Logic_unq1(I: %4: i2) -> (O: i2)
        hw.output %5 : i2
    }
}
