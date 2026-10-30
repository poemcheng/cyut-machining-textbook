import part1 from './chapters/part1.mjs';
import part2 from './chapters/part2.mjs';
import part3 from './chapters/part3.mjs';
export const chapters=[...part1,...part2,...part3];
export const references={
book:{name:'滄海書局：《製造程序》公開章節目錄（ME0348C）',url:'https://eshop.tsanghai.com.tw/products/me0348c',use:'僅用於章序與章名對應；未取得全書正文、圖表及原書題庫。'},
nptel:{name:'IIT Roorkee / NPTEL：Fundamentals of Manufacturing Processes',url:'https://nptel.ac.in/courses/112107219',use:'製程分類、材料、成形、接合與熱處理之延伸課程。'},
nptel2:{name:'IIT Kanpur / NPTEL：Manufacturing Process Technology',url:'https://nptel.ac.in/courses/112104195',use:'製造程序的原理、設備與技術脈絡。'},
sandvik:{name:'Sandvik Coromant：Turning formulas and definitions',url:'https://www.sandvik.coromant.com/en-gb/knowledge/machining-formulas-definitions/general-turning-formulas-definitions',use:'切削速度、轉速、進給與材料移除率之單位。'},
twi:{name:'TWI：Difference between heat input and arc energy',url:'https://www.twi-global.com/technical-knowledge/faqs/faq-what-is-the-difference-between-heat-input-and-arc-energy',use:'區分電弧能量與效率修正後的淨熱輸入。'},
asml:{name:'ASML：The Rayleigh criterion for resolution',url:'https://www.asml.com/en/technology/lithography-principles/rayleigh-criterion',use:'微影臨界尺寸與波長、NA、k1 的關係。'},
nist:{name:'NIST/SEMATECH：What is Process Capability?',url:'https://www.itl.nist.gov/div898/handbook/pmc/section1/pmc16.htm',use:'Cp、Cpk 的定義、穩定性與常態假設。'},
physics:{name:'OpenStax：University Physics, Stress, Strain, and Elastic Modulus',url:'https://openstax.org/books/university-physics-volume-1/pages/12-3-stress-strain-and-elastic-modulus',use:'應力、應變與線彈性近似的基礎。'},
chem:{name:'OpenStax：Chemistry 2e, Electrolysis',url:'https://openstax.org/books/chemistry-2e/pages/17-7-electrolysis',use:'電解電量、電子轉移與沉積物質量之關係。'}
};
