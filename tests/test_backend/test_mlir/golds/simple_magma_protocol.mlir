module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_magma_protocol(%I: i8) -> (O: i8) {
        hw.output %I : i8
    }
}
