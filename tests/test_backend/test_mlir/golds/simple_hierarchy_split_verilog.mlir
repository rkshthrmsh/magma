module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_comb(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) attributes {output_file = #hw.output_file<"tests/test_backend/test_mlir/build/simple_hierarchy.v">} {
        %1 = hw.constant -1 : i16
        %0 = comb.xor %1, %a : i16
        %2 = comb.or %a, %0 : i16
        %3 = comb.or %2, %b : i16
        hw.output %3, %3 : i16, i16
    }
    hw.module @simple_hierarchy(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) attributes {output_file = #hw.output_file<"tests/test_backend/test_mlir/build/simple_hierarchy.v">} {
        %0, %1 = hw.instance "simple_comb_inst0" @simple_comb(a: %a: i16, b: %b: i16, c: %c: i16) -> (y: i16, z: i16)
        hw.output %0, %1 : i16, i16
    }
}
