module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_mixed_direction_ports(%a_x: i8) -> (a_y: i8) {
        hw.output %a_x : i8
    }
}
