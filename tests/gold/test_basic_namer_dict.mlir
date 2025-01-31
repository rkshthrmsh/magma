module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module.extern @Foo(%I: i8) -> (O: i8)
    hw.module @test_basic_namer_dict(%I: i8) -> (O: i8) {
        %1 = sv.wire sym @test_basic_namer_dict.x name "x" : !hw.inout<i8>
        sv.assign %1, %I : i8
        %0 = sv.read_inout %1 : !hw.inout<i8>
        %2 = hw.instance "foo" @Foo(I: %0: i8) -> (O: i8)
        hw.output %2 : i8
    }
}
