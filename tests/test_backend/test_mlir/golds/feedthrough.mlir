module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @feedthrough(%I: i1) -> (O: i1) {
        hw.output %I : i1
    }
}
