hw.module @twizzler(%I0: i1, %I1: i1, %I2: i1) -> (%O0: i1, %O1: i1, %O2: i1) {
    %1 = hw.constant -1 : i1
    %0 = comb.xor %1, %I1 : i1
    %3 = hw.constant -1 : i1
    %2 = comb.xor %3, %I0 : i1
    %5 = hw.constant -1 : i1
    %4 = comb.xor %5, %I2 : i1
    hw.output %0, %2, %4 : i1, i1, i1
}
hw.module @twizzle(%I: i1) -> (%O: i1) {
    %2, %3, %4 = hw.instance "t0" @twizzler(%I, %0, %1) : (i1, i1, i1) -> (i1, i1, i1)
    %0, %1, %5 = hw.instance "t1" @twizzler(%2, %3, %4) : (i1, i1, i1) -> (i1, i1, i1)
    hw.output %5 : i1
}
