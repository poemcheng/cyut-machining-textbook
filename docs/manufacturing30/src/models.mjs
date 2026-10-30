/** Original teaching models; illustrative inputs, not certified machine settings. */
export function defaults(c){return Object.fromEntries(c.params.map(p=>[p[0],p[6]]));}
export function validate(c,p){for(const [k,label,unit,min,max] of c.params){if(typeof p[k]!=='number'||!Number.isFinite(p[k])||p[k]<min||p[k]>max)throw new RangeError(`${label} 必須介於 ${min}–${max} ${unit}`);}return p;}
const rad=d=>d*Math.PI/180;
export function calculate(c,p){validate(c,p);const out=[],warnings=[];const o=(key,label,value,unit='')=>out.push({key,label,value,unit});
 switch(c.id){
 case 1:{const variable=p.rate*p.cycle/3600;o('unitCost','單件成本',p.setup/p.batch+variable+p.material,'元/件');o('batchTime','整批加工時間',p.batch*p.cycle/60,'min');o('setupShare','單件設置分攤',p.setup/p.batch,'元/件');break;}
 case 2:{const V=p.length*p.width*p.height/1000,I=p.width*p.height**3/12;o('mass','試件質量',p.density*V,'g');o('deflection','樑端撓度',p.force*p.length**3/(3*p.modulus*1000*I),'mm');o('specific','比剛性 E/ρ',p.modulus/p.density,'GPa·cm³/g');if(p.force*p.length**3/(3*p.modulus*1000*I)>p.length*.05)warnings.push('撓度超過跨度 5%，小撓度樑假設可能失效。');break;}
 case 3:{const stress=p.force/p.area,strain=stress/(p.modulus*1000);o('stress','工程應力',stress,'MPa');o('strain','彈性應變',strain*100,'%');o('extension','彈性伸長估計',strain*p.length,'mm');if(stress>=p.yield)warnings.push('應力已達設定降伏強度；線彈性延伸值不再是可靠的實際變形預測。');break;}
 case 4:{const low=(p.hole-p.holeTol)-(p.shaft+p.shaftTol),high=(p.hole+p.holeTol)-(p.shaft-p.shaftTol);o('minimum','最小間隙',low,'mm');o('maximum','最大間隙',high,'mm');o('width','間隙變動範圍',high-low,'mm');warnings.push(low>=0?'極限組合屬間隙配合（含零間隙）。':high<=0?'極限組合屬過盈配合（含零間隙）。':'極限組合跨越零，屬過渡配合。');break;}
 case 5:{const r=p.radius/10,h=p.height/10,V=Math.PI*r*r*h,A=2*Math.PI*r*(r+h),M=V/A;o('solidTime','凝固時間估計',p.B*M*M,'min');o('modulus','鑄件模數 V/A',M,'cm');o('volume','鑄件體積',V,'cm³');break;}
 case 6:{const rc=2,hc=4,Vc=Math.PI*rc*rc*hc,Ac=2*Math.PI*rc*(rc+hc),r=p.radius/10,h=p.height/10,Vr=Math.PI*r*r*h,Ar=2*Math.PI*r*(r+h);o('yield','金屬利用率',100*Vc/(Vc+Vr+p.runner),'%');o('ratio','冒口/鑄件模數比',(Vr/Ar)/(Vc/Ac),'無因次');o('riser','冒口體積',Vr,'cm³');if(Vr/Ar<=Vc/Ac)warnings.push('此幾何冒口模數不大於鑄件，不能據此期待冒口最後凝固。');break;}
 case 7:{const R=p.radius,t=p.thickness,V=4*Math.PI/3*(R**3-(R-t)**3),Ro=Math.cbrt((p.expansion*R)**3),Ri=Math.cbrt(Ro**3-V*3/(4*Math.PI)),tf=Ro-Ri;o('wall','膨脹後壁厚',tf,'mm');o('stress','薄殼膜應力估計',p.pressure*Ro/(2*tf),'MPa');o('volume','玻璃體積',V/1000,'cm³');if(tf/Ro>.1)warnings.push('壁厚/半徑超過 0.1；薄殼應力式僅供趨勢比較。');break;}
 case 8:{o('clamp','理想鎖模力',p.pressure*p.area*100/1000,'kN');o('fill','理想充填時間',p.volume/p.flow,'s');o('pressure','模穴壓力',p.pressure,'MPa');break;}
 case 9:{const f=p.fraction/100;o('longitudinal','縱向彈性模數',f*p.fiber+(1-f)*p.matrix,'GPa');o('transverse','橫向彈性模數下界',1/(f/p.fiber+(1-f)/p.matrix),'GPa');o('fraction','纖維體積分率',p.fraction,'%');break;}
 case 10:{const A=Math.PI*(p.diameter/10)**2/4,h=p.mass/(p.density*p.relative/100*A);o('height','生胚高度',h*10,'mm');o('force','壓製力估計',p.pressure*A*100/1000,'kN');o('porosity','生胚孔隙率',100-p.relative,'%');break;}
 case 11:{const ratio=Math.cbrt(p.green/p.final);o('length','燒結後長度',p.length*ratio,'mm');o('shrinkage','線性收縮率',(1-ratio)*100,'%');o('volumeRatio','體積保留率',p.green/p.final*100,'%');if(p.final<=p.green)warnings.push('最終相對密度應高於生胚；目前輸入不代表正常緻密化。');break;}
 case 12:{const hf=p.height*(1-p.reduction/100),strain=Math.log(p.height/hf),avg=p.K*strain**p.n/(p.n+1),A=Math.PI*p.radius**2*p.height/hf;o('strain','真壓縮應變',strain,'無因次');o('stress','平均流動應力',avg,'MPa');o('force','理想鍛壓力',avg*A/1000,'kN');break;}
 case 13:{const dh=p.h0-p.h1;if(dh<=0)throw new RangeError('出口厚度必須小於入口厚度。');const L=Math.sqrt(p.radius*dh);o('force','理想軋延力',p.width*L*p.stress/1000,'kN');o('contact','接觸長度',L,'mm');o('velocity','出口速度',p.speed*p.h0/p.h1,'mm/s');break;}
 case 14:{const BA=rad(p.angle)*(p.radius+p.K*p.thickness);o('allowance','彎曲裕量 BA',BA,'mm');o('blank','展開長度',2*p.leg+BA,'mm');o('neutral','中性層半徑',p.radius+p.K*p.thickness,'mm');break;}
 case 15:{const r=p.uncut/p.chip,a=rad(p.rake),phi=Math.atan2(r*Math.cos(a),1-r*Math.sin(a));o('angle','剪切角',phi*180/Math.PI,'°');o('area','剪切面積',p.width*p.uncut/Math.sin(phi),'mm²');o('strain','剪切應變',1/Math.tan(phi)+Math.tan(phi-a),'無因次');break;}
 case 16:{const N=1000*p.speed/(Math.PI*p.diameter),feed=p.feed*N;o('rpm','主軸轉速',N,'rpm');o('time','有效切削時間',p.length/feed,'min');o('mrr','材料移除率（近似）',Math.PI*p.diameter*p.depth*feed/1000,'cm³/min');break;}
 case 17:{const life=(p.C/p.speed)**(1/p.n);o('life','刀具壽命估計',life,'min');o('pieces','可用切削件數',Math.floor(life/p.cycle),'件');o('speed60','60 分鐘壽命速度',p.C/(60**p.n),'m/min');break;}
 case 18:{const v=Math.PI*p.diameter*p.rpm/60000;o('wheelSpeed','砂輪周速',v,'m/s');o('mrr','材料移除率',p.width*p.depth*p.feed,'mm³/s');o('chipEq','等效切屑厚度',p.depth*p.feed/(v*1000)*1000,'μm');break;}
 case 19:{const E=.5*p.capacitance*1e-6*p.voltage**2;o('pulse','單脈衝儲能',E*1000,'mJ');o('power','有效平均功率估計',E*p.frequency*p.efficiency/100,'W');o('period','脈衝週期',1e6/p.frequency,'μs');break;}
 case 20:{if(p.initial<=p.ambient)throw new RangeError('初溫必須高於環境溫度。');const T=p.ambient+(p.initial-p.ambient)*Math.exp(-p.k*p.time);o('temperature','均溫模型溫度',T,'°C');o('cooling','瞬時降溫速率',p.k*(T-p.ambient),'°C/s');o('half','溫差半衰期',Math.log(2)/p.k,'s');break;}
 case 21:{const m=p.efficiency/100*p.current*p.time*60*63.546/(2*96485.33212);o('thickness','平均銅鍍層厚度',m/(8.96*p.area)*10000,'μm');o('mass','沉積質量',m,'g');o('charge','通過電量',p.current*p.time*60,'C');break;}
 case 22:{o('heat','淨線熱輸入',p.efficiency/100*p.voltage*p.current/(1000*p.speed),'kJ/mm');o('power','淨熱功率',p.efficiency/100*p.voltage*p.current,'W');o('arc','電弧線能量',p.voltage*p.current/(1000*p.speed),'kJ/mm');break;}
 case 23:{const Q=p.current**2*p.resistance*p.time;o('heat','理想電阻產熱',Q,'J');o('power','理想電阻功率',p.current**2*p.resistance,'W');o('cycle','通電時間',p.time,'s');break;}
 case 24:{const tau=p.force/(p.width*p.overlap);o('shear','平均剪應力',tau,'MPa');o('factor','平均應力安全係數',p.allowable/tau,'無因次');o('area','搭接面積',p.width*p.overlap,'mm²');break;}
 case 25:{const F=p.torque/(p.K*p.diameter/1000);o('preload','預緊力粗估',F/1000,'kN');o('stress','光桿截面名義應力',F/(Math.PI*p.diameter**2/4),'MPa');o('torque','鎖緊扭矩',p.torque,'N·m');break;}
 case 26:{const N=Math.ceil(p.height/p.layer),A=400*p.infill/100,time=N*(A/(.4*p.speed)+p.overhead);o('layers','列印層數',N,'層');o('time','路徑時間粗估',time/60,'min');o('volume','填充體積近似',400*p.height*p.infill/100/1000,'cm³');break;}
 case 27:{o('resolution','臨界尺寸 CD',p.k1*p.wavelength/p.NA,'nm');o('dof','焦深尺度估計',.5*p.wavelength/(p.NA*p.NA),'nm');o('wavelength','曝光波長',p.wavelength,'nm');break;}
 case 28:{const CT=Math.max(p.t1,p.t2,p.t3);o('capacity','理論產能上限',3600/CT,'件/h');o('balance','平衡效率',(p.t1+p.t2+p.t3)/(3*CT)*100,'%');o('cycle','瓶頸週期',CT,'s');break;}
 case 29:{const a=rad(p.q1),b=rad(p.q1+p.q2),x=p.L1*Math.cos(a)+p.L2*Math.cos(b),y=p.L1*Math.sin(a)+p.L2*Math.sin(b);o('x','末端 X',x,'mm');o('y','末端 Y',y,'mm');o('reach','末端距基座',Math.hypot(x,y),'mm');break;}
 case 30:{const lo=50-p.tolerance,hi=50+p.tolerance;o('cp','Cp',2*p.tolerance/(6*p.sigma),'無因次');o('cpk','Cpk',Math.min(hi-p.mean,p.mean-lo)/(3*p.sigma),'無因次');o('offset','平均值偏離目標',p.mean-50,'mm');if(p.mean<lo||p.mean>hi)warnings.push('製程平均值已在規格之外，Cpk 可為負值。');break;}
 default:throw new Error('未知章節');}
 for(const x of out)if(!Number.isFinite(x.value))throw new Error('計算值非有限數。請檢查輸入及模型。');return {outputs:out,warnings};
}
export function format(v){return Math.abs(v)>=1e5||Math.abs(v)>0&&Math.abs(v)<.001?v.toExponential(3):Number(v.toPrecision(5)).toLocaleString('zh-TW',{maximumFractionDigits:6});}
export function csvCell(v){let s=String(v??'');if(/^[\s]*[=+\-@]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}
