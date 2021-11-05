hw.module @LUT(%I: i2) -> (%O: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
    %1 = hw.constant 1 : i1
    %2 = hw.constant 1 : i1
    %3 = hw.constant 1 : i1
    %4 = hw.constant 0 : i1
    %5 = hw.array_create %1, %2, %3, %4 : i1
    %0 = hw.array_get %5[%I] : !hw.array<4xi1>
    %7 = hw.constant 1 : i1
    %8 = hw.constant 1 : i1
    %9 = hw.constant 1 : i1
    %10 = hw.constant 1 : i1
    %11 = hw.array_create %7, %8, %9, %10 : i1
    %6 = hw.array_get %11[%I] : !hw.array<4xi1>
    %13 = hw.constant 1 : i1
    %14 = hw.constant 1 : i1
    %15 = hw.constant 0 : i1
    %16 = hw.constant 1 : i1
    %17 = hw.array_create %13, %14, %15, %16 : i1
    %12 = hw.array_get %17[%I] : !hw.array<4xi1>
    %19 = hw.constant 1 : i1
    %20 = hw.constant 1 : i1
    %21 = hw.constant 1 : i1
    %22 = hw.constant 1 : i1
    %23 = hw.array_create %19, %20, %21, %22 : i1
    %18 = hw.array_get %23[%I] : !hw.array<4xi1>
    %25 = hw.constant 0 : i1
    %26 = hw.constant 0 : i1
    %27 = hw.constant 0 : i1
    %28 = hw.constant 1 : i1
    %29 = hw.array_create %25, %26, %27, %28 : i1
    %24 = hw.array_get %29[%I] : !hw.array<4xi1>
    %31 = hw.constant 0 : i1
    %32 = hw.constant 1 : i1
    %33 = hw.constant 0 : i1
    %34 = hw.constant 0 : i1
    %35 = hw.array_create %31, %32, %33, %34 : i1
    %30 = hw.array_get %35[%I] : !hw.array<4xi1>
    %37 = hw.constant 0 : i1
    %38 = hw.constant 1 : i1
    %39 = hw.constant 1 : i1
    %40 = hw.constant 0 : i1
    %41 = hw.array_create %37, %38, %39, %40 : i1
    %36 = hw.array_get %41[%I] : !hw.array<4xi1>
    %43 = hw.constant 0 : i1
    %44 = hw.constant 0 : i1
    %45 = hw.constant 0 : i1
    %46 = hw.constant 0 : i1
    %47 = hw.array_create %43, %44, %45, %46 : i1
    %42 = hw.array_get %47[%I] : !hw.array<4xi1>
    %48 = comb.concat %42, %36, %30, %24, %18, %12, %6, %0 : (i1, i1, i1, i1, i1, i1, i1, i1) -> (i8)
    %50 = hw.constant 0 : i1
    %51 = hw.constant 1 : i1
    %52 = hw.constant 1 : i1
    %53 = hw.constant 1 : i1
    %54 = hw.array_create %50, %51, %52, %53 : i1
    %49 = hw.array_get %54[%I] : !hw.array<4xi1>
    %55 = hw.struct_create (%48, %49) : !hw.struct<x: i8, y: i1>
    %57 = hw.constant 1 : i1
    %58 = hw.constant 1 : i1
    %59 = hw.constant 1 : i1
    %60 = hw.constant 0 : i1
    %61 = hw.array_create %57, %58, %59, %60 : i1
    %56 = hw.array_get %61[%I] : !hw.array<4xi1>
    %63 = hw.constant 1 : i1
    %64 = hw.constant 1 : i1
    %65 = hw.constant 0 : i1
    %66 = hw.constant 1 : i1
    %67 = hw.array_create %63, %64, %65, %66 : i1
    %62 = hw.array_get %67[%I] : !hw.array<4xi1>
    %69 = hw.constant 0 : i1
    %70 = hw.constant 0 : i1
    %71 = hw.constant 0 : i1
    %72 = hw.constant 0 : i1
    %73 = hw.array_create %69, %70, %71, %72 : i1
    %68 = hw.array_get %73[%I] : !hw.array<4xi1>
    %75 = hw.constant 1 : i1
    %76 = hw.constant 0 : i1
    %77 = hw.constant 1 : i1
    %78 = hw.constant 0 : i1
    %79 = hw.array_create %75, %76, %77, %78 : i1
    %74 = hw.array_get %79[%I] : !hw.array<4xi1>
    %81 = hw.constant 0 : i1
    %82 = hw.constant 0 : i1
    %83 = hw.constant 0 : i1
    %84 = hw.constant 1 : i1
    %85 = hw.array_create %81, %82, %83, %84 : i1
    %80 = hw.array_get %85[%I] : !hw.array<4xi1>
    %87 = hw.constant 0 : i1
    %88 = hw.constant 0 : i1
    %89 = hw.constant 0 : i1
    %90 = hw.constant 0 : i1
    %91 = hw.array_create %87, %88, %89, %90 : i1
    %86 = hw.array_get %91[%I] : !hw.array<4xi1>
    %93 = hw.constant 0 : i1
    %94 = hw.constant 1 : i1
    %95 = hw.constant 1 : i1
    %96 = hw.constant 0 : i1
    %97 = hw.array_create %93, %94, %95, %96 : i1
    %92 = hw.array_get %97[%I] : !hw.array<4xi1>
    %99 = hw.constant 1 : i1
    %100 = hw.constant 1 : i1
    %101 = hw.constant 1 : i1
    %102 = hw.constant 0 : i1
    %103 = hw.array_create %99, %100, %101, %102 : i1
    %98 = hw.array_get %103[%I] : !hw.array<4xi1>
    %104 = comb.concat %98, %92, %86, %80, %74, %68, %62, %56 : (i1, i1, i1, i1, i1, i1, i1, i1) -> (i8)
    %106 = hw.constant 0 : i1
    %107 = hw.constant 0 : i1
    %108 = hw.constant 1 : i1
    %109 = hw.constant 1 : i1
    %110 = hw.array_create %106, %107, %108, %109 : i1
    %105 = hw.array_get %110[%I] : !hw.array<4xi1>
    %111 = hw.struct_create (%104, %105) : !hw.struct<x: i8, y: i1>
    %112 = hw.array_create %111, %55 : !hw.struct<x: i8, y: i1>
    hw.output %112 : !hw.array<2x!hw.struct<x: i8, y: i1>>
}
hw.module @complex_lut(%a: i2) -> (%y: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
    %0 = hw.instance "LUT_inst0" @LUT(%a) : (i2) -> (!hw.array<2x!hw.struct<x: i8, y: i1>>)
    hw.output %0 : !hw.array<2x!hw.struct<x: i8, y: i1>>
}
