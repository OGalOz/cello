//SVG Code Start 
const svg = d3.select('svg');

//Feature: 0 
//Plasmid Arc Forward: L3S3P21
const plasmid_arc_0 = svg.append('path')
.attr('id', '2C0i7P-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#cefeae')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.0009919774719260477,
endAngle: 0.04257480601208053,
}));

//Feature: 1 
//Pointer and Text: L3S3P21 (52)
//	Pointer: 
const pointer_1 = svg.append('line')
.attr('id', '2C0i7P-pointer')
.attr('x1', '508.56966069723234')
.attr('y1', '180.1147691506619')
.attr('x2', '506.69504741971275')
.attr('y2', '250.08966339895463')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: L3S3P21 (52) 
const text_rect_1 = svg.insert('rect', 'text')
.attr('id', '2C0i7P-text-rect')
.attr('x', '500.70356164562656')
.attr('y', '160.116562418641')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: L3S3P21 (52) 
const text_1 = svg.append('text')
.attr('id', '2C0i7P-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 508.70356164562656)
.attr('y', '175.116562418641')
.text('L3S3P21 (52)');

//Feature: 2 
//Plasmid Arc Forward: Escar
const plasmid_arc_2 = svg.append('path')
.attr('id', '9W6B3a-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#706875')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.053566783484006585,
endAngle: 0.046542715899784724,
}));

//Feature: 3 
//Pointer and Text: Escar (3)
//	Pointer: 
const pointer_3 = svg.append('line')
.attr('id', '9W6B3a-pointer')
.attr('x1', '508.5291759865189')
.attr('y1', '345.23484514597294')
.attr('x2', '513.7567354621273')
.attr('y2', '250.37878249350467')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Escar (3) 
const text_rect_3 = svg.insert('rect', 'text')
.attr('id', '9W6B3a-text-rect')
.attr('x', '500.2540412772764')
.attr('y', '335.22726949610285')
.attr('width', '54.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Escar (3) 
const text_3 = svg.append('text')
.attr('id', '9W6B3a-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 508.2540412772764)
.attr('y', '350.22726949610285')
.text('Escar (3)');

//Feature: 4 
//Plasmid Arc Forward: pTac
const plasmid_arc_4 = svg.append('path')
.attr('id', '3M8M5X-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#bcdfdb')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.057534693371710764,
endAngle: 0.11697311640653411,
}));

//Feature: 5 
//Pointer and Text: pTac (70)
//	Pointer: 
const pointer_5 = svg.append('line')
.attr('id', '3M8M5X-pointer')
.attr('x1', '511.9760032257226')
.attr('y1', '370.5528086564352')
.attr('x2', '523.0307754340819')
.attr('y2', '251.06309357006765')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: pTac (70) 
const text_rect_5 = svg.insert('rect', 'text')
.attr('id', '3M8M5X-text-rect')
.attr('x', '503.51538771704094')
.attr('y', '360.53154678503387')
.attr('width', '54.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: pTac (70) 
const text_5 = svg.append('text')
.attr('id', '3M8M5X-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 511.51538771704094)
.attr('y', '375.53154678503387')
.text('pTac (70)');

//Feature: 6 
//Promoter Symbol: pTac 
const promoter_6_start_line = svg.append('line')
.attr('id', '3M8M5X-promoter-start-line')
.attr('x1', '517.8404176704287')
.attr('y1', '250.6373734952556')
.attr('x2', '519.267651084063')
.attr('y2', '230.68836337487605')
.attr('stroke', 'black')
.attr('stroke-width', '3');

const promoter_6arc = svg.append('path')
.attr('id', '3M8M5X-promoter-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '268.5',
outerRadius: '271.5',
startAngle: 0.07142237797867536,
endAngle: 0.11697311640653398,
}));

const promoter_6_arrow_1 = svg.append('line')
.attr('id', '3M8M5X-promoter-arrow-1')
.attr('x1', '525.3387878666758')
.attr('y1', '227.52129106580063')
.attr('x2', '534.1906969483015')
.attr('y2', '232.17357068020823')
.attr('stroke', 'black')
.attr('stroke-width', '3');

const promoter_6_arrow_2 = svg.append('line')
.attr('id', '3M8M5X-promoter-arrow-2')
.attr('x1', '526.7914529120065')
.attr('y1', '238.9004709835689')
.attr('x2', '534.1906969483015')
.attr('y2', '232.17357068020823')
.attr('stroke', 'black')
.attr('stroke-width', '3');

//Feature: 7 
//Plasmid Arc Forward: RiboJ53
const plasmid_arc_7 = svg.append('path')
.attr('id', '9S3w1y-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#554452')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.12796509387846017,
endAngle: 0.19533933668869186,
}));

//Feature: 8 
//Pointer and Text: RiboJ53 (78)
//	Pointer: 
const pointer_8 = svg.append('line')
.attr('id', '9S3w1y-pointer')
.attr('x1', '525.711691639083')
.attr('y1', '347.1474275222798')
.attr('x2', '541.4704703856178')
.attr('y2', '253.46359277787064')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: RiboJ53 (78) 
const text_rect_8 = svg.insert('rect', 'text')
.attr('id', '9S3w1y-text-rect')
.attr('x', '516.8822822313707')
.attr('y', '337.0781556667224')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: RiboJ53 (78) 
const text_8 = svg.append('text')
.attr('id', '9S3w1y-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 524.8822822313707)
.attr('y', '352.0781556667224')
.text('RiboJ53 (78)');

//Feature: 9 
//Plasmid Arc Forward: P3
const plasmid_arc_9 = svg.append('path')
.attr('id', '6M7o5b-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#cbbeeb')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.20633131416061792,
endAngle: 0.21319493118336072,
}));

//Feature: 10 
//Pointer and Text: P3 (17)
//	Pointer: 
const pointer_10 = svg.append('line')
.attr('id', '6M7o5b-pointer')
.attr('x1', '538.3608797767284')
.attr('y1', '324.1351572861836')
.attr('x2', '553.2789996899006')
.attr('y2', '255.74327400858832')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: P3 (17) 
const text_rect_10 = svg.insert('rect', 'text')
.attr('id', '6M7o5b-text-rect')
.attr('x', '529.2952997829304')
.attr('y', '314.0202918060118')
.attr('width', '42.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: P3 (17) 
const text_10 = svg.append('text')
.attr('id', '6M7o5b-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 537.2952997829304)
.attr('y', '329.0202918060118')
.text('P3 (17)');

//Feature: 11 
//RBS Symbol: P3 
const rbs_circle_11 = svg.append('path')
.attr('id', '6M7o5b-rbs-circle')
.attr('fill', '#bb99ff')
.attr('d','M 561.9476789166642 253.54009438280255 A 7.0 7.0 0 0 0 546.3152484532138 250.13023840264893 ');

//Feature: 12 
//Plasmid Arc Forward: PhlF
const plasmid_arc_12 = svg.append('path')
.attr('id', '7R2b5c-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#664944')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.2241869086552868,
endAngle: 0.8143332791705457,
}));

//Feature: 13 
//Pointer and Text: PhlF (605)
//	Pointer: 
const pointer_13 = svg.append('line')
.attr('id', '7R2b5c-pointer')
.attr('x1', '672.6975501337132')
.attr('y1', '201.33537842956088')
.attr('x2', '625.1431522708067')
.attr('y2', '283.5763611808412')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: PhlF (605) 
const text_rect_13 = svg.insert('rect', 'text')
.attr('id', '7R2b5c-text-rect')
.attr('x', '667.2004131791293')
.attr('y', '182.0069056531777')
.attr('width', '60.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: PhlF (605) 
const text_13 = svg.append('text')
.attr('id', '7R2b5c-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 675.2004131791293)
.attr('y', '197.0069056531777')
.text('PhlF (605)');

//Feature: 14 
//CDS Symbol: PhlF 
const cds_14_in = svg.insert('polygon')
.attr('id', '7R2b5c-cds-in')
.attr('fill', '#664944')
.attr('points', '675.7795108462559,316.64906990513794 684.084054665764,307.98682123923896 686.4601835832771,327.5221755178638 ');

const cds_14_out = svg.insert('polygon')
.attr('id', '7R2b5c-cds-out')
.attr('fill', '#664944')
.attr('points', '670.2431482999172,322.42390234907054 661.938604480409,331.0861510149695 680.5874218956149,332.954547942498 ');

//Feature: 15 
//Plasmid Arc Forward: ECK120033737
const plasmid_arc_15 = svg.append('path')
.attr('id', '8o6c3k-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#bbadbd')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.8253252566424717,
endAngle: 0.8708759950703304,
}));

//Feature: 16 
//Pointer and Text: ECK120033737 (56)
//	Pointer: 
const pointer_16 = svg.append('line')
.attr('id', '8o6c3k-pointer')
.attr('x1', '778.7295659851077')
.attr('y1', '256.6693010617988')
.attr('x2', '688.3307878277755')
.attr('y2', '335.5873655822965')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: ECK120033737 (56) 
const text_rect_16 = svg.insert('rect', 'text')
.attr('id', '8o6c3k-text-rect')
.attr('x', '774.4961817416632')
.attr('y', '238.38104837344474')
.attr('width', '102.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: ECK120033737 (56) 
const text_16 = svg.append('text')
.attr('id', '8o6c3k-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 782.4961817416632)
.attr('y', '253.38104837344474')
.text('ECK120033737 (56)');

//Feature: 17 
//Terminator Symbol: ECK120033737 
const terminator_17 = svg.insert('polygon')
.attr('id', '8o6c3k-terminator')
.attr('stroke', 'black')
.attr('stroke-width', '2')
.attr('fill', '#EA6062')
.attr('points', '689.646088903117,337.09401188491864 701.6992593240946,326.5716032821856 704.3298614747779,329.58489588743004      707.3431540800223,326.95429373674676 699.4513476279724,317.91441592101353 696.438055022728,320.5450180716968 699.0686571734113,323.55831067694123 687.0154867524337,334.08071927967427');

//Feature: 18 
//Plasmid Arc Forward: Cscar
const plasmid_arc_18 = svg.append('path')
.attr('id', '7T9u1S-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#285885')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.8818679725422565,
endAngle: 0.8748439049580347,
}));

//Feature: 19 
//Pointer and Text: Cscar (3)
//	Pointer: 
const pointer_19 = svg.append('line')
.attr('id', '7T9u1S-pointer')
.attr('x1', '619.7952801169611')
.attr('y1', '401.6430436537465')
.attr('x2', '693.2181937370341')
.attr('y2', '341.35974782862337')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Cscar (3) 
const text_rect_19 = svg.insert('rect', 'text')
.attr('id', '7T9u1S-text-rect')
.attr('x', '607.9309162422204')
.attr('y', '389.81584869717403')
.attr('width', '54.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Cscar (3) 
const text_19 = svg.append('text')
.attr('id', '7T9u1S-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 615.9309162422204)
.attr('y', '404.81584869717403')
.text('Cscar (3)');

//Feature: 20 
//Plasmid Arc Forward: Linker\1
const plasmid_arc_20 = svg.append('path')
.attr('id', '4q3m3N-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#eeddaa')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.8898037923176648,
endAngle: 0.8867476346211471,
}));

//Feature: 21 
//Pointer and Text: Linker\1 (7)
//	Pointer: 
const pointer_21 = svg.append('line')
.attr('id', '4q3m3N-pointer')
.attr('x1', '640.243282674303')
.attr('y1', '387.16462582711245')
.attr('x2', '694.7823370476431')
.attr('y2', '343.28420253765614')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Linker\1 (7) 
const text_rect_21 = svg.insert('rect', 'text')
.attr('id', '4q3m3N-text-rect')
.attr('x', '628.3476359333501')
.attr('y', '375.2989417763593')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Linker\1 (7) 
const text_21 = svg.append('text')
.attr('id', '4q3m3N-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 636.3476359333501)
.attr('y', '390.2989417763593')
.text('Linker\1 (7)');

//Feature: 22 
//Plasmid Arc Reverse: LacZ alpha
const reverse_arc_22 = svg.append('path')
.attr('id', '8Q7B2D-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#739784')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 0.9582502378805622,
endAngle: 0.9700737422629352,
}));

//Feature: 23 
//Pointer and Text: LacZ alpha (22)
//	Pointer: 
const pointer_23 = svg.append('line')
.attr('id', '8Q7B2D-pointer')
.attr('x1', '611.2955791128174')
.attr('y1', '423.59126967458104')
.attr('x2', '689.6146903403557')
.attr('y2', '369.8221631492862')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: LacZ alpha (22) 
const text_rect_23 = svg.insert('rect', 'text')
.attr('id', '8Q7B2D-text-rect')
.attr('x', '599.1735206271576')
.attr('y', '411.4212226495966')
.attr('width', '90.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: LacZ alpha (22) 
const text_23 = svg.append('text')
.attr('id', '8Q7B2D-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 607.1735206271576)
.attr('y', '426.4212226495966')
.text('LacZ alpha (22)');

//Feature: 24 
//CDS Symbol: LacZ alpha 
const cds_24_in = svg.insert('polygon')
.attr('id', '8Q7B2D-cds-in')
.attr('fill', '#739784')
.attr('points', '691.7488639877148,365.8792590259773 701.5821390640078,359.0012723093608 691.4557091456985,365.46111552596517 ');

const cds_24_out = svg.insert('polygon')
.attr('id', '8Q7B2D-cds-out')
.attr('fill', '#739784')
.attr('points', '685.1933472701861,370.4645835037217 675.3600721938931,377.3425702203383 684.910214815931,370.0607355079835 ');

//Feature: 25 
//Plasmid Arc Forward: sensor_module
const plasmid_arc_25 = svg.append('path')
.attr('id', '6V8v0k-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#aceabf')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 0.9810657197348611,
endAngle: 4.022388423379384,
}));

//Feature: 26 
//Pointer and Text: sensor_module (3076)
//	Pointer: 
const pointer_26 = svg.append('line')
.attr('id', '6V8v0k-pointer')
.attr('x1', '719.4356383716394')
.attr('y1', '797.9060264788732')
.attr('x2', '648.2673232240807')
.attr('y2', '701.2878557289683')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: sensor_module (3076) 
const text_rect_26 = svg.insert('rect', 'text')
.attr('id', '6V8v0k-text-rect')
.attr('x', '714.400984836121')
.attr('y', '786.9317835934526')
.attr('width', '120.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: sensor_module (3076) 
const text_26 = svg.append('text')
.attr('id', '6V8v0k-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 722.400984836121)
.attr('y', '801.9317835934526')
.text('sensor_module (3076)');

//Feature: 27 
//Plasmid Arc Reverse: LacZ alpha
const reverse_arc_27 = svg.append('path')
.attr('id', '0O7V1w-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#825508')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.03338040085131,
endAngle: 4.068019387087983,
}));

//Feature: 28 
//Pointer and Text: LacZ alpha (45)
//	Pointer: 
const pointer_28 = svg.append('line')
.attr('id', '0O7V1w-pointer')
.attr('x1', '393.07758691540744')
.attr('y1', '582.4172165276633')
.attr('x2', '317.83588881884225')
.attr('y2', '640.4145170471301')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: LacZ alpha (45) 
const text_rect_28 = svg.insert('rect', 'text')
.attr('id', '0O7V1w-text-rect')
.attr('x', '389.03767628891086')
.attr('y', '564.3647270266388')
.attr('width', '90.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: LacZ alpha (45) 
const text_28 = svg.append('text')
.attr('id', '0O7V1w-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 397.03767628891086)
.attr('y', '579.3647270266388')
.text('LacZ alpha (45)');

//Feature: 29 
//CDS Symbol: LacZ alpha 
const cds_29_in = svg.insert('polygon')
.attr('id', '0O7V1w-cds-in')
.attr('fill', '#825508')
.attr('points', '317.248012897466,646.1427767974704 307.8761161229771,653.6372781716997 317.9021980618665,646.9571043852604 ');

const cds_29_out = svg.insert('polygon')
.attr('id', '0O7V1w-cds-out')
.attr('fill', '#825508')
.attr('points', '323.4959440804586,641.1464425479843 332.86784085494753,633.6519411737551 324.12776394009325,641.9329298763626 ');

//Feature: 30 
//Plasmid Arc Forward: M13-fwd
const plasmid_arc_30 = svg.append('path')
.attr('id', '1s4V9p-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#aabaac')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 4.148449787594732,
endAngle: 4.155313404617474,
}));

//Feature: 31 
//Pointer and Text: M13-fwd (17)
//	Pointer: 
const pointer_31 = svg.append('line')
.attr('id', '1s4V9p-pointer')
.attr('x1', '347.0660657354482')
.attr('y1', '594.9274025261714')
.attr('x2', '287.59175796590034')
.attr('y2', '631.8436146196825')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: M13-fwd (17) 
const text_rect_31 = svg.insert('rect', 'text')
.attr('id', '1s4V9p-text-rect')
.attr('x', '343.31423057613017')
.attr('y', '577.2905302337778')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: M13-fwd (17) 
const text_31 = svg.append('text')
.attr('id', '1s4V9p-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 351.31423057613017)
.attr('y', '592.2905302337778')
.text('M13-fwd (17)');

//Feature: 32 
//Plasmid Arc Reverse: M13-rev
const reverse_arc_32 = svg.append('path')
.attr('id', '4n0m9y-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#084250')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.230783917764593,
endAngle: 4.240623467203114,
}));

//Feature: 33 
//Pointer and Text: M13-rev (20)
//	Pointer: 
const pointer_33 = svg.append('line')
.attr('id', '4n0m9y-pointer')
.attr('x1', '210.48877193365286')
.attr('y1', '647.6761620015752')
.attr('x2', '295.1151309068928')
.attr('y2', '604.5092838780379')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: M13-rev (20) 
const text_rect_33 = svg.insert('rect', 'text')
.attr('id', '4n0m9y-text-rect')
.attr('x', '198.03475304032443')
.attr('y', '634.9481029554456')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: M13-rev (20) 
const text_33 = svg.append('text')
.attr('id', '4n0m9y-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 206.03475304032443)
.attr('y', '649.9481029554456')
.text('M13-rev (20)');

//Feature: 34 
//Plasmid Arc Reverse: LacO
const reverse_arc_34 = svg.append('path')
.attr('id', '3M1D3v-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#defbdc')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.256575332034671,
endAngle: 4.268398836417044,
}));

//Feature: 35 
//Pointer and Text: LacO (22)
//	Pointer: 
const pointer_35 = svg.append('line')
.attr('id', '3M1D3v-pointer')
.attr('x1', '184.07148828158034')
.attr('y1', '650.6292650296892')
.attr('x2', '292.3898351564671')
.attr('y2', '598.9849455909387')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: LacO (22) 
const text_rect_35 = svg.insert('rect', 'text')
.attr('id', '3M1D3v-text-rect')
.attr('x', '171.55822382846006')
.attr('y', '637.7811116729705')
.attr('width', '54.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: LacO (22) 
const text_35 = svg.append('text')
.attr('id', '3M1D3v-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 179.55822382846006)
.attr('y', '652.7811116729705')
.text('LacO (22)');

//Feature: 36 
//Plasmid Arc Reverse: pLac\-10\box
const reverse_arc_36 = svg.append('path')
.attr('id', '3y8q7b-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#159556')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.283358723776674,
endAngle: 4.278318611136305,
}));

//Feature: 37 
//Pointer and Text: pLac\-10\box (5)
//	Pointer: 
const pointer_37 = svg.append('line')
.attr('id', '3y8q7b-pointer')
.attr('x1', '204.12051605300533')
.attr('y1', '634.4631212610362')
.attr('x2', '290.60836520674223')
.attr('y2', '595.1585165847333')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: pLac\-10\box (5) 
const text_rect_37 = svg.insert('rect', 'text')
.attr('id', '3y8q7b-text-rect')
.attr('x', '191.56852399228234')
.attr('y', '621.5317846650522')
.attr('width', '96.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: pLac\-10\box (5) 
const text_37 = svg.append('text')
.attr('id', '3y8q7b-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 199.56852399228234)
.attr('y', '636.5317846650522')
.text('pLac\-10\box (5)');

//Feature: 38 
//Plasmid Arc Reverse: pLac\-35\box
const reverse_arc_38 = svg.append('path')
.attr('id', '6u7V3s-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#fffeae')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.3071661831029,
endAngle: 4.3021260704625295,
}));

//Feature: 39 
//Pointer and Text: pLac\-35\box (5)
//	Pointer: 
const pointer_39 = svg.append('line')
.attr('id', '6u7V3s-pointer')
.attr('x1', '224.00317605280995')
.attr('y1', '617.58296292858')
.attr('x2', '288.40243497382096')
.attr('y2', '590.1469382452447')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: pLac\-35\box (5) 
const text_rect_39 = svg.insert('rect', 'text')
.attr('id', '6u7V3s-text-rect')
.attr('x', '211.40322898702345')
.attr('y', '604.5426789773896')
.attr('width', '96.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: pLac\-35\box (5) 
const text_39 = svg.append('text')
.attr('id', '6u7V3s-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 219.40322898702345)
.attr('y', '619.5426789773896')
.text('pLac\-35\box (5)');

//Feature: 40 
//Plasmid Arc Reverse: CAP\site
const reverse_arc_40 = svg.append('path')
.attr('id', '9X5I8p-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#981946')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.330973642429124,
endAngle: 4.334861327036089,
}));

//Feature: 41 
//Pointer and Text: CAP\site (14)
//	Pointer: 
const pointer_41 = svg.append('line')
.attr('id', '9X5I8p-pointer')
.attr('x1', '197.52215271337738')
.attr('y1', '618.8787277053831')
.attr('x2', '285.9387542279286')
.attr('y2', '584.129561145348')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: CAP\site (14) 
const text_rect_41 = svg.insert('rect', 'text')
.attr('id', '9X5I8p-text-rect')
.attr('x', '184.86864737050627')
.attr('y', '605.7076312085428')
.attr('width', '78.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: CAP\site (14) 
const text_41 = svg.append('text')
.attr('id', '9X5I8p-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 192.86864737050627)
.attr('y', '620.7076312085428')
.text('CAP\site (14)');

//Feature: 42 
//Plasmid Arc Reverse: Center\LacO3
const reverse_arc_42 = svg.append('path')
.attr('id', '6G6A5F-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#ccdffb')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.357757034171128,
endAngle: 4.347757034171128,
}));

//Feature: 43 
//Pointer and Text: Center\LacO3 (0)
//	Pointer: 
const pointer_43 = svg.append('line')
.attr('id', '6G6A5F-pointer')
.attr('x1', '171.7789749596873')
.attr('y1', '621.5358330760374')
.attr('x2', '284.3118978306517')
.attr('y2', '579.8664045928246')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Center\LacO3 (0) 
const text_rect_43 = svg.insert('rect', 'text')
.attr('id', '6G6A5F-text-rect')
.attr('x', '159.09010317339713')
.attr('y', '608.272059262838')
.attr('width', '96.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Center\LacO3 (0) 
const text_43 = svg.append('text')
.attr('id', '6G6A5F-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 167.09010317339713)
.attr('y', '623.272059262838')
.text('Center\LacO3 (0)');

//Feature: 44 
//Plasmid Arc Reverse: LacI
const reverse_arc_44 = svg.append('path')
.attr('id', '8J4T6J-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#213475')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.360732966586906,
endAngle: 4.357676808890388,
}));

//Feature: 45 
//Pointer and Text: LacI (7)
//	Pointer: 
const pointer_45 = svg.append('line')
.attr('id', '8J4T6J-pointer')
.attr('x1', '194.50200383433912')
.attr('y1', '610.8872144963785')
.attr('x2', '283.8014180981477')
.attr('y2', '578.4740287205141')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: LacI (7) 
const text_rect_45 = svg.insert('rect', 'text')
.attr('id', '8J4T6J-text-rect')
.attr('x', '181.80203466255972')
.attr('y', '597.5931716424767')
.attr('width', '48.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: LacI (7) 
const text_45 = svg.append('text')
.attr('id', '8J4T6J-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 189.80203466255972)
.attr('y', '612.5931716424767')
.text('LacI (7)');

//Feature: 46 
//Plasmid Arc Forward: Linker\2
const plasmid_arc_46 = svg.append('path')
.attr('id', '8T8m0c-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#ceaefe')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 4.428187434677877,
endAngle: 4.42513127698136,
}));

//Feature: 47 
//Pointer and Text: Linker\2 (7)
//	Pointer: 
const pointer_47 = svg.append('line')
.attr('id', '8T8m0c-pointer')
.attr('x1', '192.526865071469')
.attr('y1', '588.6581710685562')
.attr('x2', '259.78661333708516')
.attr('y2', '569.2641961473095')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Linker\2 (7) 
const text_rect_47 = svg.insert('rect', 'text')
.attr('id', '8T8m0c-text-rect')
.attr('x', '179.7225973382107')
.attr('y', '575.0434549915024')
.attr('width', '72.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Linker\2 (7) 
const text_47 = svg.append('text')
.attr('id', '8T8m0c-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 187.7225973382107)
.attr('y', '590.0434549915024')
.text('Linker\2 (7)');

//Feature: 48 
//Plasmid Arc Forward: cc
const plasmid_arc_48 = svg.append('path')
.attr('id', '2y3r9q-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#640730')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '246.0',
outerRadius: '254.0',
startAngle: 4.436123254453285,
endAngle: 4.429099186869064,
}));

//Feature: 49 
//Pointer and Text: cc (3)
//	Pointer: 
const pointer_49 = svg.append('line')
.attr('id', '2y3r9q-pointer')
.attr('x1', '167.94249472830836')
.attr('y1', '593.6098990104168')
.attr('x2', '259.3786193683394')
.attr('y2', '567.833260152476')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: cc (3) 
const text_rect_49 = svg.insert('rect', 'text')
.attr('id', '2y3r9q-text-rect')
.attr('x', '155.13006711567516')
.attr('y', '579.9665642134663')
.attr('width', '36.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: cc (3) 
const text_49 = svg.append('text')
.attr('id', '2y3r9q-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 163.13006711567516)
.attr('y', '594.9665642134663')
.text('cc (3)');

//Feature: 50 
//Plasmid Arc Reverse: origin
const reverse_arc_50 = svg.append('path')
.attr('id', '5j2K1v-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#cabfdb')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 4.747604180638064,
endAngle: 4.737604180638065,
}));

//Feature: 51 
//Pointer and Text: origin (0)
//	Pointer: 
const pointer_51 = svg.append('line')
.attr('id', '5j2K1v-pointer')
.attr('x1', '390.0681990197926')
.attr('y1', '496.1271285526022')
.attr('x2', '270.1425979504754')
.attr('y2', '491.90217788271366')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: origin (0) 
const text_rect_51 = svg.insert('rect', 'text')
.attr('id', '5j2K1v-text-rect')
.attr('x', '387.06509906434746')
.attr('y', '481.30316816384754')
.attr('width', '60.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: origin (0) 
const text_51 = svg.append('text')
.attr('id', '5j2K1v-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 395.06509906434746)
.attr('y', '496.30316816384754')
.text('origin (0)');

//Feature: 52 
//Plasmid Arc Reverse: Kanamycin\phosphotransferase
const reverse_arc_52 = svg.append('path')
.attr('id', '6P9O3b-arc')
.attr('transform', 'translate(500,500)')
.attr('fill', '#708399')
.attr('stroke-width', '8')
.attr('d', d3.arc() ({
innerRadius: '226.0',
outerRadius: '234.0',
startAngle: 5.376517897839179,
endAngle: 6.174979537458908,
}));

//Feature: 53 
//Pointer and Text: Kanamycin\phosphotransferase (815)
//	Pointer: 
const pointer_53 = svg.append('line')
.attr('id', '6P9O3b-pointer')
.attr('x1', '434.9890730564085')
.attr('y1', '381.6844077142197')
.attr('x2', '389.2406429849922')
.attr('y2', '298.42528721681873')
.attr('stroke', 'black')
.attr('stroke-width', '1');

//	 Text-Box: Kanamycin\phosphotransferase (815) 
const text_rect_53 = svg.insert('rect', 'text')
.attr('id', '6P9O3b-text-rect')
.attr('x', '429.3968851654304')
.attr('y', '371.0664666877671')
.attr('width', '204.0')
.attr('height', '19')
.attr('stroke', 'gray')
.attr('fill', 'white');

//	 Text: Kanamycin\phosphotransferase (815) 
const text_53 = svg.append('text')
.attr('id', '6P9O3b-text')
.attr('font-weight', 'normal')
.attr('font-size', '9').attr('x', 437.3968851654304)
.attr('y', '386.0664666877671')
.text('Kanamycin\phosphotransferase (815)');

//Feature: 54 
//CDS Symbol: Kanamycin\phosphotransferase 
const cds_54_in = svg.insert('polygon')
.attr('id', '6P9O3b-cds-in')
.attr('fill', '#708399')
.attr('points', '327.9854776774265,341.35888266235366 319.16422012242276,333.2234407476026 315.7357649476318,355.76861755995816 ');

const cds_54_out = svg.insert('polygon')
.attr('id', '6P9O3b-cds-out')
.attr('fill', '#708399')
.attr('points', '333.866316047429,346.78251060552105 342.68757360243274,354.91795252027214 322.0353969152341,360.69960499380574 ');

//Feature: 55 
//Plasmid Gap Arc: g
const gap_arc_55 = svg.append('path')
.attr('id', '5V1P9H-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 0.8858358824299606,
endAngle: 0.8788118148457387,
}));

//Feature: 56 
//Plasmid Gap Arc: g
const gap_arc_56 = svg.append('path')
.attr('id', '1N6X3K-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 0.8977396120930731,
endAngle: 0.947258260408636,
}));

//Feature: 57 
//Plasmid Gap Arc: g
const gap_arc_57 = svg.append('path')
.attr('id', '4w3R4L-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.079011364559908,
endAngle: 4.137457810122806,
}));

//Feature: 58 
//Plasmid Gap Arc: g
const gap_arc_58 = svg.append('path')
.attr('id', '8X7C6F-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.1663053820894005,
endAngle: 4.219791940292668,
}));

//Feature: 59 
//Plasmid Gap Arc: g
const gap_arc_59 = svg.append('path')
.attr('id', '2q9n4f-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.25161544467504,
endAngle: 4.245583354562745,
}));

//Feature: 60 
//Plasmid Gap Arc: g
const gap_arc_60 = svg.append('path')
.attr('id', '3r3d1B-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.27939081388897,
endAngle: 4.272366746304748,
}));

//Feature: 61 
//Plasmid Gap Arc: g
const gap_arc_61 = svg.append('path')
.attr('id', '9N3P9W-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.28931058860823,
endAngle: 4.296174205630973,
}));

//Feature: 62 
//Plasmid Gap Arc: g
const gap_arc_62 = svg.append('path')
.attr('id', '1T2I7X-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.313118047934456,
endAngle: 4.319981664957198,
}));

//Feature: 63 
//Plasmid Gap Arc: g
const gap_arc_63 = svg.append('path')
.attr('id', '3d0m2J-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.345853304508015,
endAngle: 4.346765056699201,
}));

//Feature: 64 
//Plasmid Gap Arc: g
const gap_arc_64 = svg.append('path')
.attr('id', '3o2f1g-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.358749011643054,
endAngle: 4.349740989114981,
}));

//Feature: 65 
//Plasmid Gap Arc: g
const gap_arc_65 = svg.append('path')
.attr('id', '1I3L0L-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.3686687863623135,
endAngle: 4.417195457205951,
}));

//Feature: 66 
//Plasmid Gap Arc: g
const gap_arc_66 = svg.append('path')
.attr('id', '2l1p0Z-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.4400911643409895,
endAngle: 4.736612203166139,
}));

//Feature: 67 
//Plasmid Gap Arc: g
const gap_arc_67 = svg.append('path')
.attr('id', '4r6u5o-gap')
.attr('transform', 'translate(500,500)')
.attr('fill', 'black')
.attr('stroke-width', '3')
.attr('d', d3.arc() ({
innerRadius: '248.5',
outerRadius: '251.5',
startAngle: 4.74859615810999,
endAngle: 5.3655259203672525,
}));

//Feature: 68 
//Center Text: 
const center_name = svg.append('text')
.attr('id', 'plasmid_center_text-name')
.attr('font-weight', 'bold')
.attr('font-size', '20pt').attr('x', 350.0)
.attr('y', '485')
.text('plasmid_circuit_P000');

const center_length = svg.append('text')
.attr('id', 'plasmid_center_text-length')
.attr('font-weight', 'bold')
.attr('font-size', '20pt').attr('x', 447.5)
.attr('y', '515')
.text('6334 bp');

