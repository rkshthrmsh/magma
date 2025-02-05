module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_aggregates_array(%a: !hw.array<8xi16>) -> (y: !hw.array<8xi16>, z: !hw.array<4xi16>) {
        %1 = hw.constant 4 : i3
        %0 = hw.array_slice %a[%1] : (!hw.array<8xi16>) -> !hw.array<4xi16>
        %3 = hw.constant 0 : i3
        %2 = hw.array_slice %a[%3] : (!hw.array<8xi16>) -> !hw.array<4xi16>
        %4 = hw.array_concat %2, %0 : !hw.array<4xi16>, !hw.array<4xi16>
        hw.output %4, %2 : !hw.array<8xi16>, !hw.array<4xi16>
    }
}
