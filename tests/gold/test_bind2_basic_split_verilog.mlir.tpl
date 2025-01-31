module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @TopBasicAsserts_mlir(%I: i1, %O: i1, %other: i1) -> () attributes {output_file = #hw.output_file<"$cwd/build/TopBasicAsserts_mlir.v">, output_filelist = #hw.output_filelist<"$cwd/build/test_bind2_basic_split_verilog_bind_files.list">} {
    }
    hw.module @Top(%I: i1) -> (O: i1) attributes {output_file = #hw.output_file<"$cwd/build/test_bind2_basic_split_verilog.v">} {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I : i1
        hw.instance "TopBasicAsserts_mlir_inst0" sym @Top.TopBasicAsserts_mlir_inst0 @TopBasicAsserts_mlir(I: %I: i1, O: %0: i1, other: %I: i1) -> () {doNotPrint = true}
        hw.output %0 : i1
    }
    sv.bind #hw.innerNameRef<@Top::@Top.TopBasicAsserts_mlir_inst0> {output_file = #hw.output_file<"$cwd/build/TopBasicAsserts_mlir.v">}
}
