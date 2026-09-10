var Bi={LEFT:0,MIDDLE:1,RIGHT:2,ROTATE:0,DOLLY:1,PAN:2},ki={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},yu=0,hc=1,xu=2;var Ds=1,Su=2,Hr=3,li=0,xn=1,ci=2,hi=0,Wr=1,uc=2,dc=3,fc=4,bu=5;var ar=100,Mu=101,Eu=102,wu=103,Tu=104,Au=200,Cu=201,Ru=202,Pu=203,pc=204,mc=205,Iu=206,Du=207,Lu=208,Fu=209,Nu=210,Uu=211,Ou=212,Bu=213,ku=214,Ua=0,Oa=1,Ba=2,Pr=3,ka=4,za=5,Va=6,Ga=7,vo=0,zu=1,Vu=2,Jn=0,gc=1,_c=2,vc=3,yc=4,xc=5,Sc=6,bc=7;var Mc=300,zi=301,or=302,yo=303,xo=304,Ls=306,Ha=1e3,si=1001,Wa=1002,an=1003,Gu=1004;var Fs=1005;var ln=1006,So=1007;var Vi=1008;var En=1009,Ec=1010,wc=1011,Xr=1012,bo=1013,Kn=1014,Qn=1015,ei=1016,Mo=1017,Eo=1018,$r=1020,Tc=35902,Ac=35899,Cc=1021,Rc=1022,kn=1023,ai=1026,Gi=1027,Pc=1028,wo=1029,Hi=1030,To=1031;var Ao=1033,Ns=33776,Us=33777,Os=33778,Bs=33779,Co=35840,Ro=35841,Po=35842,Io=35843,Do=36196,Lo=37492,Fo=37496,No=37488,Uo=37489,ks=37490,Oo=37491,Bo=37808,ko=37809,zo=37810,Vo=37811,Go=37812,Ho=37813,Wo=37814,Xo=37815,$o=37816,jo=37817,qo=37818,Yo=37819,Zo=37820,Jo=37821,Ko=36492,Qo=36494,el=36495,tl=36283,nl=36284,zs=36285,il=36286;var hs=2300,Xa=2301,Fa=2302,nc=2303,ic=2400,rc=2401,sc=2402;var Hu=3200;var rl=0,Wu=1,bi="",dn="srgb",us="srgb-linear",ds="linear",It="srgb";var Na=7680;var Xu=519,$u=512,ju=513,qu=514,sl=515,Yu=516,Zu=517,al=518,Ju=519,Ku=35044;var Ic="300 es",Yn=2e3,Ir=2001;function Q_(i){for(let e=i.length-1;e>=0;--e)if(i[e]>=65535)return!0;return!1}function e0(i){return ArrayBuffer.isView(i)&&!(i instanceof DataView)}function fs(i){return document.createElementNS("http://www.w3.org/1999/xhtml",i)}function Qu(){let i=fs("canvas");return i.style.display="block",i}var Wh={},Dr=null;function Dc(...i){let e="THREE."+i.shift();Dr?Dr("log",e,...i):console.log(e,...i)}function ed(i){let e=i[0];if(typeof e=="string"&&e.startsWith("TSL:")){let t=i[1];t&&t.isStackTrace?i[0]+=" "+t.getLocation():i[1]='Stack trace not available. Enable "THREE.Node.captureStackTrace" to capture stack traces.'}return i}function et(...i){i=ed(i);let e="THREE."+i.shift();if(Dr)Dr("warn",e,...i);else{let t=i[0];t&&t.isStackTrace?console.warn(t.getError(e)):console.warn(e,...i)}}function it(...i){i=ed(i);let e="THREE."+i.shift();if(Dr)Dr("error",e,...i);else{let t=i[0];t&&t.isStackTrace?console.error(t.getError(e)):console.error(e,...i)}}function nr(...i){let e=i.join(" ");e in Wh||(Wh[e]=!0,et(...i))}function td(i,e,t){return new Promise(function(n,s){function o(){switch(i.clientWaitSync(e,i.SYNC_FLUSH_COMMANDS_BIT,0)){case i.WAIT_FAILED:s();break;case i.TIMEOUT_EXPIRED:setTimeout(o,t);break;default:n()}}setTimeout(o,t)})}var nd={[Ua]:Oa,[Ba]:Va,[ka]:Ga,[Pr]:za,[Oa]:Ua,[Va]:Ba,[Ga]:ka,[za]:Pr},Zn=class{addEventListener(e,t){this._listeners===void 0&&(this._listeners={});let n=this._listeners;n[e]===void 0&&(n[e]=[]),n[e].indexOf(t)===-1&&n[e].push(t)}hasEventListener(e,t){let n=this._listeners;return n===void 0?!1:n[e]!==void 0&&n[e].indexOf(t)!==-1}removeEventListener(e,t){let n=this._listeners;if(n===void 0)return;let s=n[e];if(s!==void 0){let o=s.indexOf(t);o!==-1&&s.splice(o,1)}}dispatchEvent(e){let t=this._listeners;if(t===void 0)return;let n=t[e.type];if(n!==void 0){e.target=this;let s=n.slice(0);for(let o=0,l=s.length;o<l;o++)s[o].call(this,e);e.target=null}}},hn=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Xh=1234567,ls=Math.PI/180,Lr=180/Math.PI;function jr(){let i=Math.random()*4294967295|0,e=Math.random()*4294967295|0,t=Math.random()*4294967295|0,n=Math.random()*4294967295|0;return(hn[i&255]+hn[i>>8&255]+hn[i>>16&255]+hn[i>>24&255]+"-"+hn[e&255]+hn[e>>8&255]+"-"+hn[e>>16&15|64]+hn[e>>24&255]+"-"+hn[t&63|128]+hn[t>>8&255]+"-"+hn[t>>16&255]+hn[t>>24&255]+hn[n&255]+hn[n>>8&255]+hn[n>>16&255]+hn[n>>24&255]).toLowerCase()}function _t(i,e,t){return Math.max(e,Math.min(t,i))}function Lc(i,e){return(i%e+e)%e}function t0(i,e,t,n,s){return n+(i-e)*(s-n)/(t-e)}function n0(i,e,t){return i!==e?(t-i)/(e-i):0}function cs(i,e,t){return(1-t)*i+t*e}function i0(i,e,t,n){return cs(i,e,1-Math.exp(-t*n))}function r0(i,e=1){return e-Math.abs(Lc(i,e*2)-e)}function s0(i,e,t){return i<=e?0:i>=t?1:(i=(i-e)/(t-e),i*i*(3-2*i))}function a0(i,e,t){return i<=e?0:i>=t?1:(i=(i-e)/(t-e),i*i*i*(i*(i*6-15)+10))}function o0(i,e){return i+Math.floor(Math.random()*(e-i+1))}function l0(i,e){return i+Math.random()*(e-i)}function c0(i){return i*(.5-Math.random())}function h0(i){i!==void 0&&(Xh=i);let e=Xh+=1831565813;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}function u0(i){return i*ls}function d0(i){return i*Lr}function f0(i){return i>0&&Number.isInteger(i)&&2**Math.round(Math.log2(i))===i}function p0(i){return Math.pow(2,Math.ceil(Math.log(i)/Math.LN2))}function m0(i){return Math.pow(2,Math.floor(Math.log(i)/Math.LN2))}function g0(i,e,t,n,s){let o=Math.cos,l=Math.sin,h=o(t/2),d=l(t/2),f=o((e+n)/2),g=l((e+n)/2),y=o((e-n)/2),m=l((e-n)/2),S=o((n-e)/2),T=l((n-e)/2);switch(s){case"XYX":i.set(h*g,d*y,d*m,h*f);break;case"YZY":i.set(d*m,h*g,d*y,h*f);break;case"ZXZ":i.set(d*y,d*m,h*g,h*f);break;case"XZX":i.set(h*g,d*T,d*S,h*f);break;case"YXY":i.set(d*S,h*g,d*T,h*f);break;case"ZYZ":i.set(d*T,d*S,h*g,h*f);break;default:et("MathUtils: .setQuaternionFromProperEuler() encountered an unknown order: "+s)}}function Cr(i,e){switch(e.constructor){case Float32Array:return i;case Uint32Array:return i/4294967295;case Uint16Array:return i/65535;case Uint8Array:case Uint8ClampedArray:return i/255;case Int32Array:return Math.max(i/2147483647,-1);case Int16Array:return Math.max(i/32767,-1);case Int8Array:return Math.max(i/127,-1);default:throw new Error("THREE.MathUtils: Invalid component type.")}}function _n(i,e){switch(e.constructor){case Float32Array:return i;case Uint32Array:return Math.round(i*4294967295);case Uint16Array:return Math.round(i*65535);case Uint8Array:case Uint8ClampedArray:return Math.round(i*255);case Int32Array:return Math.round(i*2147483647);case Int16Array:return Math.round(i*32767);case Int8Array:return Math.round(i*127);default:throw new Error("THREE.MathUtils: Invalid component type.")}}var Fc={DEG2RAD:ls,RAD2DEG:Lr,generateUUID:jr,clamp:_t,euclideanModulo:Lc,mapLinear:t0,inverseLerp:n0,lerp:cs,damp:i0,pingpong:r0,smoothstep:s0,smootherstep:a0,randInt:o0,randFloat:l0,randFloatSpread:c0,seededRandom:h0,degToRad:u0,radToDeg:d0,isPowerOfTwo:f0,ceilPowerOfTwo:p0,floorPowerOfTwo:m0,setQuaternionFromProperEuler:g0,normalize:_n,denormalize:Cr},nt=class i{static{i.prototype.isVector2=!0}constructor(e=0,t=0){this.x=e,this.y=t}get width(){return this.x}set width(e){this.x=e}get height(){return this.y}set height(e){this.y=e}set(e,t){return this.x=e,this.y=t,this}setScalar(e){return this.x=e,this.y=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;default:throw new Error("THREE.Vector2: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;default:throw new Error("THREE.Vector2: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y)}copy(e){return this.x=e.x,this.y=e.y,this}add(e){return this.x+=e.x,this.y+=e.y,this}addScalar(e){return this.x+=e,this.y+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this}subScalar(e){return this.x-=e,this.y-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this}multiply(e){return this.x*=e.x,this.y*=e.y,this}multiplyScalar(e){return this.x*=e,this.y*=e,this}divide(e){return this.x/=e.x,this.y/=e.y,this}divideScalar(e){return this.multiplyScalar(1/e)}applyMatrix3(e){let t=this.x,n=this.y,s=e.elements;return this.x=s[0]*t+s[3]*n+s[6],this.y=s[1]*t+s[4]*n+s[7],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this}clamp(e,t){return this.x=_t(this.x,e.x,t.x),this.y=_t(this.y,e.y,t.y),this}clampScalar(e,t){return this.x=_t(this.x,e,t),this.y=_t(this.y,e,t),this}clampLength(e,t){let n=this.length();return this.divideScalar(n||1).multiplyScalar(_t(n,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(e){return this.x*e.x+this.y*e.y}cross(e){return this.x*e.y-this.y*e.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let n=this.dot(e)/t;return Math.acos(_t(n,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,n=this.y-e.y;return t*t+n*n}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this}equals(e){return e.x===this.x&&e.y===this.y}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this}rotateAround(e,t){let n=Math.cos(t),s=Math.sin(t),o=this.x-e.x,l=this.y-e.y;return this.x=o*n-l*s+e.x,this.y=o*s+l*n+e.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}},In=class{constructor(e=0,t=0,n=0,s=1){this.isQuaternion=!0,this._x=e,this._y=t,this._z=n,this._w=s}static slerpFlat(e,t,n,s,o,l,h){let d=n[s+0],f=n[s+1],g=n[s+2],y=n[s+3],m=o[l+0],S=o[l+1],T=o[l+2],P=o[l+3];if(y!==P||d!==m||f!==S||g!==T){let b=d*m+f*S+g*T+y*P;b<0&&(m=-m,S=-S,T=-T,P=-P,b=-b);let _=1-h;if(b<.9995){let U=Math.acos(b),z=Math.sin(U);_=Math.sin(_*U)/z,h=Math.sin(h*U)/z,d=d*_+m*h,f=f*_+S*h,g=g*_+T*h,y=y*_+P*h}else{d=d*_+m*h,f=f*_+S*h,g=g*_+T*h,y=y*_+P*h;let U=1/Math.sqrt(d*d+f*f+g*g+y*y);d*=U,f*=U,g*=U,y*=U}}e[t]=d,e[t+1]=f,e[t+2]=g,e[t+3]=y}static multiplyQuaternionsFlat(e,t,n,s,o,l){let h=n[s],d=n[s+1],f=n[s+2],g=n[s+3],y=o[l],m=o[l+1],S=o[l+2],T=o[l+3];return e[t]=h*T+g*y+d*S-f*m,e[t+1]=d*T+g*m+f*y-h*S,e[t+2]=f*T+g*S+h*m-d*y,e[t+3]=g*T-h*y-d*m-f*S,e}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get w(){return this._w}set w(e){this._w=e,this._onChangeCallback()}set(e,t,n,s){return this._x=e,this._y=t,this._z=n,this._w=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(e){return this._x=e.x,this._y=e.y,this._z=e.z,this._w=e.w,this._onChangeCallback(),this}setFromEuler(e,t=!0){let n=e._x,s=e._y,o=e._z,l=e._order,h=Math.cos,d=Math.sin,f=h(n/2),g=h(s/2),y=h(o/2),m=d(n/2),S=d(s/2),T=d(o/2);switch(l){case"XYZ":this._x=m*g*y+f*S*T,this._y=f*S*y-m*g*T,this._z=f*g*T+m*S*y,this._w=f*g*y-m*S*T;break;case"YXZ":this._x=m*g*y+f*S*T,this._y=f*S*y-m*g*T,this._z=f*g*T-m*S*y,this._w=f*g*y+m*S*T;break;case"ZXY":this._x=m*g*y-f*S*T,this._y=f*S*y+m*g*T,this._z=f*g*T+m*S*y,this._w=f*g*y-m*S*T;break;case"ZYX":this._x=m*g*y-f*S*T,this._y=f*S*y+m*g*T,this._z=f*g*T-m*S*y,this._w=f*g*y+m*S*T;break;case"YZX":this._x=m*g*y+f*S*T,this._y=f*S*y+m*g*T,this._z=f*g*T-m*S*y,this._w=f*g*y-m*S*T;break;case"XZY":this._x=m*g*y-f*S*T,this._y=f*S*y-m*g*T,this._z=f*g*T+m*S*y,this._w=f*g*y+m*S*T;break;default:et("Quaternion: .setFromEuler() encountered an unknown order: "+l)}return t===!0&&this._onChangeCallback(),this}setFromAxisAngle(e,t){let n=t/2,s=Math.sin(n);return this._x=e.x*s,this._y=e.y*s,this._z=e.z*s,this._w=Math.cos(n),this._onChangeCallback(),this}setFromRotationMatrix(e){let t=e.elements,n=t[0],s=t[4],o=t[8],l=t[1],h=t[5],d=t[9],f=t[2],g=t[6],y=t[10],m=n+h+y;if(m>0){let S=.5/Math.sqrt(m+1);this._w=.25/S,this._x=(g-d)*S,this._y=(o-f)*S,this._z=(l-s)*S}else if(n>h&&n>y){let S=2*Math.sqrt(1+n-h-y);this._w=(g-d)/S,this._x=.25*S,this._y=(s+l)/S,this._z=(o+f)/S}else if(h>y){let S=2*Math.sqrt(1+h-n-y);this._w=(o-f)/S,this._x=(s+l)/S,this._y=.25*S,this._z=(d+g)/S}else{let S=2*Math.sqrt(1+y-n-h);this._w=(l-s)/S,this._x=(o+f)/S,this._y=(d+g)/S,this._z=.25*S}return this._onChangeCallback(),this}setFromUnitVectors(e,t){let n=e.dot(t)+1;return n<1e-8?(n=0,Math.abs(e.x)>Math.abs(e.z)?(this._x=-e.y,this._y=e.x,this._z=0,this._w=n):(this._x=0,this._y=-e.z,this._z=e.y,this._w=n)):(this._x=e.y*t.z-e.z*t.y,this._y=e.z*t.x-e.x*t.z,this._z=e.x*t.y-e.y*t.x,this._w=n),this.normalize()}angleTo(e){return 2*Math.acos(Math.abs(_t(this.dot(e),-1,1)))}rotateTowards(e,t){let n=this.angleTo(e);if(n===0)return this;let s=Math.min(1,t/n);return this.slerp(e,s),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(e){return this._x*e._x+this._y*e._y+this._z*e._z+this._w*e._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let e=this.length();return e===0?(this._x=0,this._y=0,this._z=0,this._w=1):(e=1/e,this._x=this._x*e,this._y=this._y*e,this._z=this._z*e,this._w=this._w*e),this._onChangeCallback(),this}multiply(e){return this.multiplyQuaternions(this,e)}premultiply(e){return this.multiplyQuaternions(e,this)}multiplyQuaternions(e,t){let n=e._x,s=e._y,o=e._z,l=e._w,h=t._x,d=t._y,f=t._z,g=t._w;return this._x=n*g+l*h+s*f-o*d,this._y=s*g+l*d+o*h-n*f,this._z=o*g+l*f+n*d-s*h,this._w=l*g-n*h-s*d-o*f,this._onChangeCallback(),this}slerp(e,t){let n=e._x,s=e._y,o=e._z,l=e._w,h=this.dot(e);h<0&&(n=-n,s=-s,o=-o,l=-l,h=-h);let d=1-t;if(h<.9995){let f=Math.acos(h),g=Math.sin(f);d=Math.sin(d*f)/g,t=Math.sin(t*f)/g,this._x=this._x*d+n*t,this._y=this._y*d+s*t,this._z=this._z*d+o*t,this._w=this._w*d+l*t,this._onChangeCallback()}else this._x=this._x*d+n*t,this._y=this._y*d+s*t,this._z=this._z*d+o*t,this._w=this._w*d+l*t,this.normalize();return this}slerpQuaternions(e,t,n){return this.copy(e).slerp(t,n)}random(){let e=2*Math.PI*Math.random(),t=2*Math.PI*Math.random(),n=Math.random(),s=Math.sqrt(1-n),o=Math.sqrt(n);return this.set(s*Math.sin(e),s*Math.cos(e),o*Math.sin(t),o*Math.cos(t))}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._w===this._w}fromArray(e,t=0){return this._x=e[t],this._y=e[t+1],this._z=e[t+2],this._w=e[t+3],this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._w,e}fromBufferAttribute(e,t){return this._x=e.getX(t),this._y=e.getY(t),this._z=e.getZ(t),this._w=e.getW(t),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},j=class i{static{i.prototype.isVector3=!0}constructor(e=0,t=0,n=0){this.x=e,this.y=t,this.z=n}set(e,t,n){return n===void 0&&(n=this.z),this.x=e,this.y=t,this.z=n,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;default:throw new Error("THREE.Vector3: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("THREE.Vector3: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this}multiplyVectors(e,t){return this.x=e.x*t.x,this.y=e.y*t.y,this.z=e.z*t.z,this}applyEuler(e){return this.applyQuaternion($h.setFromEuler(e))}applyAxisAngle(e,t){return this.applyQuaternion($h.setFromAxisAngle(e,t))}applyMatrix3(e){let t=this.x,n=this.y,s=this.z,o=e.elements;return this.x=o[0]*t+o[3]*n+o[6]*s,this.y=o[1]*t+o[4]*n+o[7]*s,this.z=o[2]*t+o[5]*n+o[8]*s,this}applyNormalMatrix(e){return this.applyMatrix3(e).normalize()}applyMatrix4(e){let t=this.x,n=this.y,s=this.z,o=e.elements,l=1/(o[3]*t+o[7]*n+o[11]*s+o[15]);return this.x=(o[0]*t+o[4]*n+o[8]*s+o[12])*l,this.y=(o[1]*t+o[5]*n+o[9]*s+o[13])*l,this.z=(o[2]*t+o[6]*n+o[10]*s+o[14])*l,this}applyQuaternion(e){let t=this.x,n=this.y,s=this.z,o=e.x,l=e.y,h=e.z,d=e.w,f=2*(l*s-h*n),g=2*(h*t-o*s),y=2*(o*n-l*t);return this.x=t+d*f+l*y-h*g,this.y=n+d*g+h*f-o*y,this.z=s+d*y+o*g-l*f,this}project(e){return this.applyMatrix4(e.matrixWorldInverse).applyMatrix4(e.projectionMatrix)}unproject(e){return this.applyMatrix4(e.projectionMatrixInverse).applyMatrix4(e.matrixWorld)}transformDirection(e){let t=this.x,n=this.y,s=this.z,o=e.elements;return this.x=o[0]*t+o[4]*n+o[8]*s,this.y=o[1]*t+o[5]*n+o[9]*s,this.z=o[2]*t+o[6]*n+o[10]*s,this.normalize()}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this}divideScalar(e){return this.multiplyScalar(1/e)}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this}clamp(e,t){return this.x=_t(this.x,e.x,t.x),this.y=_t(this.y,e.y,t.y),this.z=_t(this.z,e.z,t.z),this}clampScalar(e,t){return this.x=_t(this.x,e,t),this.y=_t(this.y,e,t),this.z=_t(this.z,e,t),this}clampLength(e,t){let n=this.length();return this.divideScalar(n||1).multiplyScalar(_t(n,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this.z=e.z+(t.z-e.z)*n,this}cross(e){return this.crossVectors(this,e)}crossVectors(e,t){let n=e.x,s=e.y,o=e.z,l=t.x,h=t.y,d=t.z;return this.x=s*d-o*h,this.y=o*l-n*d,this.z=n*h-s*l,this}projectOnVector(e){let t=e.lengthSq();if(t===0)return this.set(0,0,0);let n=e.dot(this)/t;return this.copy(e).multiplyScalar(n)}projectOnPlane(e){return Ll.copy(this).projectOnVector(e),this.sub(Ll)}reflect(e){return this.sub(Ll.copy(e).multiplyScalar(2*this.dot(e)))}angleTo(e){let t=Math.sqrt(this.lengthSq()*e.lengthSq());if(t===0)return Math.PI/2;let n=this.dot(e)/t;return Math.acos(_t(n,-1,1))}distanceTo(e){return Math.sqrt(this.distanceToSquared(e))}distanceToSquared(e){let t=this.x-e.x,n=this.y-e.y,s=this.z-e.z;return t*t+n*n+s*s}manhattanDistanceTo(e){return Math.abs(this.x-e.x)+Math.abs(this.y-e.y)+Math.abs(this.z-e.z)}setFromSpherical(e){return this.setFromSphericalCoords(e.radius,e.phi,e.theta)}setFromSphericalCoords(e,t,n){let s=Math.sin(t)*e;return this.x=s*Math.sin(n),this.y=Math.cos(t)*e,this.z=s*Math.cos(n),this}setFromCylindrical(e){return this.setFromCylindricalCoords(e.radius,e.theta,e.y)}setFromCylindricalCoords(e,t,n){return this.x=e*Math.sin(t),this.y=n,this.z=e*Math.cos(t),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this}setFromMatrixScale(e){let t=this.setFromMatrixColumn(e,0).length(),n=this.setFromMatrixColumn(e,1).length(),s=this.setFromMatrixColumn(e,2).length();return this.x=t,this.y=n,this.z=s,this}setFromMatrixColumn(e,t){return this.fromArray(e.elements,t*4)}setFromMatrix3Column(e,t){return this.fromArray(e.elements,t*3)}setFromEuler(e){return this.x=e._x,this.y=e._y,this.z=e._z,this}setFromColor(e){return this.x=e.r,this.y=e.g,this.z=e.b,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let e=Math.random()*Math.PI*2,t=Math.random()*2-1,n=Math.sqrt(1-t*t);return this.x=n*Math.cos(e),this.y=t,this.z=n*Math.sin(e),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}},Ll=new j,$h=new In,at=class i{static{i.prototype.isMatrix3=!0}constructor(e,t,n,s,o,l,h,d,f){this.elements=[1,0,0,0,1,0,0,0,1],e!==void 0&&this.set(e,t,n,s,o,l,h,d,f)}set(e,t,n,s,o,l,h,d,f){let g=this.elements;return g[0]=e,g[1]=s,g[2]=h,g[3]=t,g[4]=o,g[5]=d,g[6]=n,g[7]=l,g[8]=f,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(e){let t=this.elements,n=e.elements;return t[0]=n[0],t[1]=n[1],t[2]=n[2],t[3]=n[3],t[4]=n[4],t[5]=n[5],t[6]=n[6],t[7]=n[7],t[8]=n[8],this}extractBasis(e,t,n){return e.setFromMatrix3Column(this,0),t.setFromMatrix3Column(this,1),n.setFromMatrix3Column(this,2),this}setFromMatrix4(e){let t=e.elements;return this.set(t[0],t[4],t[8],t[1],t[5],t[9],t[2],t[6],t[10]),this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let n=e.elements,s=t.elements,o=this.elements,l=n[0],h=n[3],d=n[6],f=n[1],g=n[4],y=n[7],m=n[2],S=n[5],T=n[8],P=s[0],b=s[3],_=s[6],U=s[1],z=s[4],R=s[7],I=s[2],L=s[5],B=s[8];return o[0]=l*P+h*U+d*I,o[3]=l*b+h*z+d*L,o[6]=l*_+h*R+d*B,o[1]=f*P+g*U+y*I,o[4]=f*b+g*z+y*L,o[7]=f*_+g*R+y*B,o[2]=m*P+S*U+T*I,o[5]=m*b+S*z+T*L,o[8]=m*_+S*R+T*B,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[3]*=e,t[6]*=e,t[1]*=e,t[4]*=e,t[7]*=e,t[2]*=e,t[5]*=e,t[8]*=e,this}determinant(){let e=this.elements,t=e[0],n=e[1],s=e[2],o=e[3],l=e[4],h=e[5],d=e[6],f=e[7],g=e[8];return t*l*g-t*h*f-n*o*g+n*h*d+s*o*f-s*l*d}invert(){let e=this.elements,t=e[0],n=e[1],s=e[2],o=e[3],l=e[4],h=e[5],d=e[6],f=e[7],g=e[8],y=g*l-h*f,m=h*d-g*o,S=f*o-l*d,T=t*y+n*m+s*S;if(T===0)return this.set(0,0,0,0,0,0,0,0,0);let P=1/T;return e[0]=y*P,e[1]=(s*f-g*n)*P,e[2]=(h*n-s*l)*P,e[3]=m*P,e[4]=(g*t-s*d)*P,e[5]=(s*o-h*t)*P,e[6]=S*P,e[7]=(n*d-f*t)*P,e[8]=(l*t-n*o)*P,this}transpose(){let e,t=this.elements;return e=t[1],t[1]=t[3],t[3]=e,e=t[2],t[2]=t[6],t[6]=e,e=t[5],t[5]=t[7],t[7]=e,this}getNormalMatrix(e){return this.setFromMatrix4(e).invert().transpose()}transposeIntoArray(e){let t=this.elements;return e[0]=t[0],e[1]=t[3],e[2]=t[6],e[3]=t[1],e[4]=t[4],e[5]=t[7],e[6]=t[2],e[7]=t[5],e[8]=t[8],this}setUvTransform(e,t,n,s,o,l,h){let d=Math.cos(o),f=Math.sin(o);return this.set(n*d,n*f,-n*(d*l+f*h)+l+e,-s*f,s*d,-s*(-f*l+d*h)+h+t,0,0,1),this}scale(e,t){return nr("Matrix3: .scale() is deprecated. Use .makeScale() instead."),this.premultiply(Fl.makeScale(e,t)),this}rotate(e){return nr("Matrix3: .rotate() is deprecated. Use .makeRotation() instead."),this.premultiply(Fl.makeRotation(-e)),this}translate(e,t){return nr("Matrix3: .translate() is deprecated. Use .makeTranslation() instead."),this.premultiply(Fl.makeTranslation(e,t)),this}makeTranslation(e,t){return e.isVector2?this.set(1,0,e.x,0,1,e.y,0,0,1):this.set(1,0,e,0,1,t,0,0,1),this}makeRotation(e){let t=Math.cos(e),n=Math.sin(e);return this.set(t,-n,0,n,t,0,0,0,1),this}makeScale(e,t){return this.set(e,0,0,0,t,0,0,0,1),this}equals(e){let t=this.elements,n=e.elements;for(let s=0;s<9;s++)if(t[s]!==n[s])return!1;return!0}fromArray(e,t=0){for(let n=0;n<9;n++)this.elements[n]=e[n+t];return this}toArray(e=[],t=0){let n=this.elements;return e[t]=n[0],e[t+1]=n[1],e[t+2]=n[2],e[t+3]=n[3],e[t+4]=n[4],e[t+5]=n[5],e[t+6]=n[6],e[t+7]=n[7],e[t+8]=n[8],e}clone(){return new this.constructor().fromArray(this.elements)}},Fl=new at,jh=new at().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),qh=new at().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function _0(){let i={enabled:!0,workingColorSpace:us,spaces:{},convert:function(s,o,l){return this.enabled===!1||o===l||!o||!l||(this.spaces[o].transfer===It&&(s.r=yi(s.r),s.g=yi(s.g),s.b=yi(s.b)),this.spaces[o].primaries!==this.spaces[l].primaries&&(s.applyMatrix3(this.spaces[o].toXYZ),s.applyMatrix3(this.spaces[l].fromXYZ)),this.spaces[l].transfer===It&&(s.r=Rr(s.r),s.g=Rr(s.g),s.b=Rr(s.b))),s},workingToColorSpace:function(s,o){return this.convert(s,this.workingColorSpace,o)},colorSpaceToWorking:function(s,o){return this.convert(s,o,this.workingColorSpace)},getPrimaries:function(s){return this.spaces[s].primaries},getTransfer:function(s){return s===bi?ds:this.spaces[s].transfer},getToneMappingMode:function(s){return this.spaces[s].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(s,o=this.workingColorSpace){return s.fromArray(this.spaces[o].luminanceCoefficients)},define:function(s){Object.assign(this.spaces,s)},_getMatrix:function(s,o,l){return s.copy(this.spaces[o].toXYZ).multiply(this.spaces[l].fromXYZ)},_getDrawingBufferColorSpace:function(s){return this.spaces[s].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(s=this.workingColorSpace){return this.spaces[s].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(s,o){return nr("ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),i.workingToColorSpace(s,o)},toWorkingColorSpace:function(s,o){return nr("ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),i.colorSpaceToWorking(s,o)}},e=[.64,.33,.3,.6,.15,.06],t=[.2126,.7152,.0722],n=[.3127,.329];return i.define({[us]:{primaries:e,whitePoint:n,transfer:ds,toXYZ:jh,fromXYZ:qh,luminanceCoefficients:t,workingColorSpaceConfig:{unpackColorSpace:dn},outputColorSpaceConfig:{drawingBufferColorSpace:dn}},[dn]:{primaries:e,whitePoint:n,transfer:It,toXYZ:jh,fromXYZ:qh,luminanceCoefficients:t,outputColorSpaceConfig:{drawingBufferColorSpace:dn}}}),i}var xt=_0();function yi(i){return i<.04045?i*.0773993808:Math.pow(i*.9478672986+.0521327014,2.4)}function Rr(i){return i<.0031308?i*12.92:1.055*Math.pow(i,.41666)-.055}var mr,$a=class{static getDataURL(e,t="image/png"){if(/^data:/i.test(e.src)||typeof HTMLCanvasElement>"u")return e.src;let n;if(e instanceof HTMLCanvasElement)n=e;else{mr===void 0&&(mr=fs("canvas")),mr.width=e.width,mr.height=e.height;let s=mr.getContext("2d");e instanceof ImageData?s.putImageData(e,0,0):s.drawImage(e,0,0,e.width,e.height),n=mr}return n.toDataURL(t)}static sRGBToLinear(e){if(typeof HTMLImageElement<"u"&&e instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&e instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&e instanceof ImageBitmap){let t=fs("canvas");t.width=e.width,t.height=e.height;let n=t.getContext("2d");n.drawImage(e,0,0,e.width,e.height);let s=n.getImageData(0,0,e.width,e.height),o=s.data;for(let l=0;l<o.length;l++)o[l]=yi(o[l]/255)*255;return n.putImageData(s,0,0),t}else if(e.data){let t=e.data.slice(0);for(let n=0;n<t.length;n++)t instanceof Uint8Array||t instanceof Uint8ClampedArray?t[n]=Math.floor(yi(t[n]/255)*255):t[n]=yi(t[n]);return{data:t,width:e.width,height:e.height}}else return et("ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),e}},v0=0,Fr=class{constructor(e=null){this.isTextureSource=!0,Object.defineProperty(this,"id",{value:v0++}),this.uuid=jr(),this.data=e,this.dataReady=!0,this.version=0}getSize(e){let t=this.data;return typeof HTMLVideoElement<"u"&&t instanceof HTMLVideoElement?e.set(t.videoWidth,t.videoHeight,0):typeof VideoFrame<"u"&&t instanceof VideoFrame?e.set(t.displayWidth,t.displayHeight,0):t!==null?e.set(t.width,t.height,t.depth||0):e.set(0,0,0),e}set needsUpdate(e){e===!0&&this.version++}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.images[this.uuid]!==void 0)return e.images[this.uuid];let n={uuid:this.uuid,url:""},s=this.data;if(s!==null){let o;if(Array.isArray(s)){o=[];for(let l=0,h=s.length;l<h;l++)s[l].isDataTexture?o.push(Nl(s[l].image)):o.push(Nl(s[l]))}else o=Nl(s);n.url=o}return t||(e.images[this.uuid]=n),n}};function Nl(i){return typeof HTMLImageElement<"u"&&i instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&i instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&i instanceof ImageBitmap?$a.getDataURL(i):i.data?{data:Array.from(i.data),width:i.width,height:i.height,type:i.data.constructor.name}:(et("Texture: Unable to serialize Texture."),{})}var y0=0,Ul=new j,bn=class i extends Zn{constructor(e=i.DEFAULT_IMAGE,t=i.DEFAULT_MAPPING,n=si,s=si,o=ln,l=Vi,h=kn,d=En,f=i.DEFAULT_ANISOTROPY,g=bi){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:y0++}),this.uuid=jr(),this.name="",this.source=new Fr(e),this.mipmaps=[],this.mapping=t,this.channel=0,this.wrapS=n,this.wrapT=s,this.magFilter=o,this.minFilter=l,this.anisotropy=f,this.format=h,this.internalFormat=null,this.type=d,this.offset=new nt(0,0),this.repeat=new nt(1,1),this.center=new nt(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new at,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=g,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(e&&e.depth&&e.depth>1),this.pmremVersion=0,this.normalized=!1}get width(){return this.source.getSize(Ul).x}get height(){return this.source.getSize(Ul).y}get depth(){return this.source.getSize(Ul).z}get image(){return this.source.data}set image(e){this.source.data=e}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(e){return this.name=e.name,this.source=e.source,this.mipmaps=e.mipmaps.slice(0),this.mapping=e.mapping,this.channel=e.channel,this.wrapS=e.wrapS,this.wrapT=e.wrapT,this.magFilter=e.magFilter,this.minFilter=e.minFilter,this.anisotropy=e.anisotropy,this.format=e.format,this.internalFormat=e.internalFormat,this.type=e.type,this.normalized=e.normalized,this.offset.copy(e.offset),this.repeat.copy(e.repeat),this.center.copy(e.center),this.rotation=e.rotation,this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrix.copy(e.matrix),this.generateMipmaps=e.generateMipmaps,this.premultiplyAlpha=e.premultiplyAlpha,this.flipY=e.flipY,this.unpackAlignment=e.unpackAlignment,this.colorSpace=e.colorSpace,this.renderTarget=e.renderTarget,this.isRenderTargetTexture=e.isRenderTargetTexture,this.isArrayTexture=e.isArrayTexture,this.userData=JSON.parse(JSON.stringify(e.userData)),this.needsUpdate=!0,this}setValues(e){for(let t in e){let n=e[t];if(n===void 0){et(`Texture.setValues(): parameter '${t}' has value of undefined.`);continue}let s=this[t];if(s===void 0){et(`Texture.setValues(): property '${t}' does not exist.`);continue}s&&n&&s.isVector2&&n.isVector2||s&&n&&s.isVector3&&n.isVector3||s&&n&&s.isMatrix3&&n.isMatrix3?s.copy(n):this[t]=n}}toJSON(e){let t=e===void 0||typeof e=="string";if(!t&&e.textures[this.uuid]!==void 0)return e.textures[this.uuid];let n={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(e).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,normalized:this.normalized,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(n.userData=this.userData),t||(e.textures[this.uuid]=n),n}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(e){if(this.mapping!==Mc)return e;if(e.applyMatrix3(this.matrix),e.x<0||e.x>1)switch(this.wrapS){case Ha:e.x=e.x-Math.floor(e.x);break;case si:e.x=e.x<0?0:1;break;case Wa:Math.abs(Math.floor(e.x)%2)===1?e.x=Math.ceil(e.x)-e.x:e.x=e.x-Math.floor(e.x);break}if(e.y<0||e.y>1)switch(this.wrapT){case Ha:e.y=e.y-Math.floor(e.y);break;case si:e.y=e.y<0?0:1;break;case Wa:Math.abs(Math.floor(e.y)%2)===1?e.y=Math.ceil(e.y)-e.y:e.y=e.y-Math.floor(e.y);break}return this.flipY&&(e.y=1-e.y),e}set needsUpdate(e){e===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(e){e===!0&&this.pmremVersion++}};bn.DEFAULT_IMAGE=null;bn.DEFAULT_MAPPING=Mc;bn.DEFAULT_ANISOTROPY=1;var Ht=class i{static{i.prototype.isVector4=!0}constructor(e=0,t=0,n=0,s=1){this.x=e,this.y=t,this.z=n,this.w=s}get width(){return this.z}set width(e){this.z=e}get height(){return this.w}set height(e){this.w=e}set(e,t,n,s){return this.x=e,this.y=t,this.z=n,this.w=s,this}setScalar(e){return this.x=e,this.y=e,this.z=e,this.w=e,this}setX(e){return this.x=e,this}setY(e){return this.y=e,this}setZ(e){return this.z=e,this}setW(e){return this.w=e,this}setComponent(e,t){switch(e){case 0:this.x=t;break;case 1:this.y=t;break;case 2:this.z=t;break;case 3:this.w=t;break;default:throw new Error("THREE.Vector4: index is out of range: "+e)}return this}getComponent(e){switch(e){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("THREE.Vector4: index is out of range: "+e)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(e){return this.x=e.x,this.y=e.y,this.z=e.z,this.w=e.w!==void 0?e.w:1,this}add(e){return this.x+=e.x,this.y+=e.y,this.z+=e.z,this.w+=e.w,this}addScalar(e){return this.x+=e,this.y+=e,this.z+=e,this.w+=e,this}addVectors(e,t){return this.x=e.x+t.x,this.y=e.y+t.y,this.z=e.z+t.z,this.w=e.w+t.w,this}addScaledVector(e,t){return this.x+=e.x*t,this.y+=e.y*t,this.z+=e.z*t,this.w+=e.w*t,this}sub(e){return this.x-=e.x,this.y-=e.y,this.z-=e.z,this.w-=e.w,this}subScalar(e){return this.x-=e,this.y-=e,this.z-=e,this.w-=e,this}subVectors(e,t){return this.x=e.x-t.x,this.y=e.y-t.y,this.z=e.z-t.z,this.w=e.w-t.w,this}multiply(e){return this.x*=e.x,this.y*=e.y,this.z*=e.z,this.w*=e.w,this}multiplyScalar(e){return this.x*=e,this.y*=e,this.z*=e,this.w*=e,this}applyMatrix4(e){let t=this.x,n=this.y,s=this.z,o=this.w,l=e.elements;return this.x=l[0]*t+l[4]*n+l[8]*s+l[12]*o,this.y=l[1]*t+l[5]*n+l[9]*s+l[13]*o,this.z=l[2]*t+l[6]*n+l[10]*s+l[14]*o,this.w=l[3]*t+l[7]*n+l[11]*s+l[15]*o,this}divide(e){return this.x/=e.x,this.y/=e.y,this.z/=e.z,this.w/=e.w,this}divideScalar(e){return this.multiplyScalar(1/e)}setAxisAngleFromQuaternion(e){this.w=2*Math.acos(e.w);let t=Math.sqrt(1-e.w*e.w);return t<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=e.x/t,this.y=e.y/t,this.z=e.z/t),this}setAxisAngleFromRotationMatrix(e){let t,n,s,o,d=e.elements,f=d[0],g=d[4],y=d[8],m=d[1],S=d[5],T=d[9],P=d[2],b=d[6],_=d[10];if(Math.abs(g-m)<.01&&Math.abs(y-P)<.01&&Math.abs(T-b)<.01){if(Math.abs(g+m)<.1&&Math.abs(y+P)<.1&&Math.abs(T+b)<.1&&Math.abs(f+S+_-3)<.1)return this.set(1,0,0,0),this;t=Math.PI;let z=(f+1)/2,R=(S+1)/2,I=(_+1)/2,L=(g+m)/4,B=(y+P)/4,w=(T+b)/4;return z>R&&z>I?z<.01?(n=0,s=.707106781,o=.707106781):(n=Math.sqrt(z),s=L/n,o=B/n):R>I?R<.01?(n=.707106781,s=0,o=.707106781):(s=Math.sqrt(R),n=L/s,o=w/s):I<.01?(n=.707106781,s=.707106781,o=0):(o=Math.sqrt(I),n=B/o,s=w/o),this.set(n,s,o,t),this}let U=Math.sqrt((b-T)*(b-T)+(y-P)*(y-P)+(m-g)*(m-g));return Math.abs(U)<.001&&(U=1),this.x=(b-T)/U,this.y=(y-P)/U,this.z=(m-g)/U,this.w=Math.acos((f+S+_-1)/2),this}setFromMatrixPosition(e){let t=e.elements;return this.x=t[12],this.y=t[13],this.z=t[14],this.w=t[15],this}min(e){return this.x=Math.min(this.x,e.x),this.y=Math.min(this.y,e.y),this.z=Math.min(this.z,e.z),this.w=Math.min(this.w,e.w),this}max(e){return this.x=Math.max(this.x,e.x),this.y=Math.max(this.y,e.y),this.z=Math.max(this.z,e.z),this.w=Math.max(this.w,e.w),this}clamp(e,t){return this.x=_t(this.x,e.x,t.x),this.y=_t(this.y,e.y,t.y),this.z=_t(this.z,e.z,t.z),this.w=_t(this.w,e.w,t.w),this}clampScalar(e,t){return this.x=_t(this.x,e,t),this.y=_t(this.y,e,t),this.z=_t(this.z,e,t),this.w=_t(this.w,e,t),this}clampLength(e,t){let n=this.length();return this.divideScalar(n||1).multiplyScalar(_t(n,e,t))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(e){return this.x*e.x+this.y*e.y+this.z*e.z+this.w*e.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(e){return this.normalize().multiplyScalar(e)}lerp(e,t){return this.x+=(e.x-this.x)*t,this.y+=(e.y-this.y)*t,this.z+=(e.z-this.z)*t,this.w+=(e.w-this.w)*t,this}lerpVectors(e,t,n){return this.x=e.x+(t.x-e.x)*n,this.y=e.y+(t.y-e.y)*n,this.z=e.z+(t.z-e.z)*n,this.w=e.w+(t.w-e.w)*n,this}equals(e){return e.x===this.x&&e.y===this.y&&e.z===this.z&&e.w===this.w}fromArray(e,t=0){return this.x=e[t],this.y=e[t+1],this.z=e[t+2],this.w=e[t+3],this}toArray(e=[],t=0){return e[t]=this.x,e[t+1]=this.y,e[t+2]=this.z,e[t+3]=this.w,e}fromBufferAttribute(e,t){return this.x=e.getX(t),this.y=e.getY(t),this.z=e.getZ(t),this.w=e.getW(t),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}},ja=class extends Zn{constructor(e=1,t=1,n={}){super(),n=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:ln,depthBuffer:!0,stencilBuffer:!1,resolveColorBuffer:!0,resolveDepthBuffer:!0,resolveStencilBuffer:!0,storeMultisampledColorBuffer:!0,storeMultisampledDepthBuffer:!0,storeMultisampledStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1,useArrayDepthTexture:!1},n),this.isRenderTarget=!0,this.width=e,this.height=t,this.depth=n.depth,this.scissor=new Ht(0,0,e,t),this.scissorTest=!1,this.viewport=new Ht(0,0,e,t),this.textures=[];let s={width:e,height:t,depth:n.depth},o=new bn(s),l=n.count;for(let h=0;h<l;h++)this.textures[h]=o.clone(),this.textures[h].isRenderTargetTexture=!0,this.textures[h].renderTarget=this;this._setTextureOptions(n),this.depthBuffer=n.depthBuffer,this.stencilBuffer=n.stencilBuffer,this.resolveColorBuffer=n.resolveColorBuffer,this.resolveDepthBuffer=n.resolveDepthBuffer,this.resolveStencilBuffer=n.resolveStencilBuffer,this.storeMultisampledColorBuffer=n.storeMultisampledColorBuffer,this.storeMultisampledDepthBuffer=n.storeMultisampledDepthBuffer,this.storeMultisampledStencilBuffer=n.storeMultisampledStencilBuffer,this._depthTexture=null,this.depthTexture=n.depthTexture,this.samples=n.samples,this.multiview=n.multiview,this.useArrayDepthTexture=n.useArrayDepthTexture}_setTextureOptions(e={}){let t={minFilter:ln,generateMipmaps:!1,flipY:!1,internalFormat:null};e.mapping!==void 0&&(t.mapping=e.mapping),e.wrapS!==void 0&&(t.wrapS=e.wrapS),e.wrapT!==void 0&&(t.wrapT=e.wrapT),e.wrapR!==void 0&&(t.wrapR=e.wrapR),e.magFilter!==void 0&&(t.magFilter=e.magFilter),e.minFilter!==void 0&&(t.minFilter=e.minFilter),e.format!==void 0&&(t.format=e.format),e.type!==void 0&&(t.type=e.type),e.anisotropy!==void 0&&(t.anisotropy=e.anisotropy),e.colorSpace!==void 0&&(t.colorSpace=e.colorSpace),e.flipY!==void 0&&(t.flipY=e.flipY),e.generateMipmaps!==void 0&&(t.generateMipmaps=e.generateMipmaps),e.internalFormat!==void 0&&(t.internalFormat=e.internalFormat);for(let n=0;n<this.textures.length;n++)this.textures[n].setValues(t)}get texture(){return this.textures[0]}set texture(e){this.textures[0]=e}set depthTexture(e){this._depthTexture!==null&&this._depthTexture.renderTarget===this&&(this._depthTexture.renderTarget=null),e!==null&&e.renderTarget===null&&(e.renderTarget=this),this._depthTexture=e}get depthTexture(){return this._depthTexture}setSize(e,t,n=1){if(this.width!==e||this.height!==t||this.depth!==n){this.width=e,this.height=t,this.depth=n;for(let s=0,o=this.textures.length;s<o;s++)this.textures[s].image.width=e,this.textures[s].image.height=t,this.textures[s].image.depth=n,this.textures[s].isData3DTexture!==!0&&(this.textures[s].isArrayTexture=this.textures[s].image.depth>1);this.dispose()}this.viewport.set(0,0,e,t),this.scissor.set(0,0,e,t)}clone(){return new this.constructor().copy(this)}copy(e){this.width=e.width,this.height=e.height,this.depth=e.depth,this.scissor.copy(e.scissor),this.scissorTest=e.scissorTest,this.viewport.copy(e.viewport),this.textures.length=0;for(let t=0,n=e.textures.length;t<n;t++){this.textures[t]=e.textures[t].clone(),this.textures[t].isRenderTargetTexture=!0,this.textures[t].renderTarget=this;let s=Object.assign({},e.textures[t].image);this.textures[t].source=new Fr(s)}if(this.depthBuffer=e.depthBuffer,this.stencilBuffer=e.stencilBuffer,this.resolveColorBuffer=e.resolveColorBuffer,this.resolveDepthBuffer=e.resolveDepthBuffer,this.resolveStencilBuffer=e.resolveStencilBuffer,this.storeMultisampledColorBuffer=e.storeMultisampledColorBuffer,this.storeMultisampledDepthBuffer=e.storeMultisampledDepthBuffer,this.storeMultisampledStencilBuffer=e.storeMultisampledStencilBuffer,e.depthTexture!==null)if(e.depthTexture.renderTarget===e){let t=e.depthTexture.clone();t.renderTarget=null,this.depthTexture=t}else this.depthTexture=e.depthTexture;return this.samples=e.samples,this.multiview=e.multiview,this.useArrayDepthTexture=e.useArrayDepthTexture,this}dispose(){this.dispatchEvent({type:"dispose"})}},Mn=class extends ja{constructor(e=1,t=1,n={}){super(e,t,n),this.isWebGLRenderTarget=!0}},ps=class extends bn{constructor(e=null,t=1,n=1,s=1){super(null),this.isDataArrayTexture=!0,this.image={data:e,width:t,height:n,depth:s},this.magFilter=an,this.minFilter=an,this.wrapR=si,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}copy(e){return super.copy(e),this.wrapR=e.wrapR,this}addLayerUpdate(e){this.layerUpdates.add(e)}clearLayerUpdates(){this.layerUpdates.clear()}};var qa=class extends bn{constructor(e=null,t=1,n=1,s=1){super(null),this.isData3DTexture=!0,this.image={data:e,width:t,height:n,depth:s},this.magFilter=an,this.minFilter=an,this.wrapR=si,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}copy(e){return super.copy(e),this.wrapR=e.wrapR,this}};var Ot=class i{static{i.prototype.isMatrix4=!0}constructor(e,t,n,s,o,l,h,d,f,g,y,m,S,T,P,b){this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],e!==void 0&&this.set(e,t,n,s,o,l,h,d,f,g,y,m,S,T,P,b)}set(e,t,n,s,o,l,h,d,f,g,y,m,S,T,P,b){let _=this.elements;return _[0]=e,_[4]=t,_[8]=n,_[12]=s,_[1]=o,_[5]=l,_[9]=h,_[13]=d,_[2]=f,_[6]=g,_[10]=y,_[14]=m,_[3]=S,_[7]=T,_[11]=P,_[15]=b,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new i().fromArray(this.elements)}copy(e){let t=this.elements,n=e.elements;return t[0]=n[0],t[1]=n[1],t[2]=n[2],t[3]=n[3],t[4]=n[4],t[5]=n[5],t[6]=n[6],t[7]=n[7],t[8]=n[8],t[9]=n[9],t[10]=n[10],t[11]=n[11],t[12]=n[12],t[13]=n[13],t[14]=n[14],t[15]=n[15],this}copyPosition(e){let t=this.elements,n=e.elements;return t[12]=n[12],t[13]=n[13],t[14]=n[14],this}setFromMatrix3(e){let t=e.elements;return this.set(t[0],t[3],t[6],0,t[1],t[4],t[7],0,t[2],t[5],t[8],0,0,0,0,1),this}extractBasis(e,t,n){return this.determinantAffine()===0?(e.set(1,0,0),t.set(0,1,0),n.set(0,0,1),this):(e.setFromMatrixColumn(this,0),t.setFromMatrixColumn(this,1),n.setFromMatrixColumn(this,2),this)}makeBasis(e,t,n){return this.set(e.x,t.x,n.x,0,e.y,t.y,n.y,0,e.z,t.z,n.z,0,0,0,0,1),this}extractRotation(e){if(e.determinantAffine()===0)return this.identity();let t=this.elements,n=e.elements,s=1/gr.setFromMatrixColumn(e,0).length(),o=1/gr.setFromMatrixColumn(e,1).length(),l=1/gr.setFromMatrixColumn(e,2).length();return t[0]=n[0]*s,t[1]=n[1]*s,t[2]=n[2]*s,t[3]=0,t[4]=n[4]*o,t[5]=n[5]*o,t[6]=n[6]*o,t[7]=0,t[8]=n[8]*l,t[9]=n[9]*l,t[10]=n[10]*l,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromEuler(e){let t=this.elements,n=e.x,s=e.y,o=e.z,l=Math.cos(n),h=Math.sin(n),d=Math.cos(s),f=Math.sin(s),g=Math.cos(o),y=Math.sin(o);if(e.order==="XYZ"){let m=l*g,S=l*y,T=h*g,P=h*y;t[0]=d*g,t[4]=-d*y,t[8]=f,t[1]=S+T*f,t[5]=m-P*f,t[9]=-h*d,t[2]=P-m*f,t[6]=T+S*f,t[10]=l*d}else if(e.order==="YXZ"){let m=d*g,S=d*y,T=f*g,P=f*y;t[0]=m+P*h,t[4]=T*h-S,t[8]=l*f,t[1]=l*y,t[5]=l*g,t[9]=-h,t[2]=S*h-T,t[6]=P+m*h,t[10]=l*d}else if(e.order==="ZXY"){let m=d*g,S=d*y,T=f*g,P=f*y;t[0]=m-P*h,t[4]=-l*y,t[8]=T+S*h,t[1]=S+T*h,t[5]=l*g,t[9]=P-m*h,t[2]=-l*f,t[6]=h,t[10]=l*d}else if(e.order==="ZYX"){let m=l*g,S=l*y,T=h*g,P=h*y;t[0]=d*g,t[4]=T*f-S,t[8]=m*f+P,t[1]=d*y,t[5]=P*f+m,t[9]=S*f-T,t[2]=-f,t[6]=h*d,t[10]=l*d}else if(e.order==="YZX"){let m=l*d,S=l*f,T=h*d,P=h*f;t[0]=d*g,t[4]=P-m*y,t[8]=T*y+S,t[1]=y,t[5]=l*g,t[9]=-h*g,t[2]=-f*g,t[6]=S*y+T,t[10]=m-P*y}else if(e.order==="XZY"){let m=l*d,S=l*f,T=h*d,P=h*f;t[0]=d*g,t[4]=-y,t[8]=f*g,t[1]=m*y+P,t[5]=l*g,t[9]=S*y-T,t[2]=T*y-S,t[6]=h*g,t[10]=P*y+m}return t[3]=0,t[7]=0,t[11]=0,t[12]=0,t[13]=0,t[14]=0,t[15]=1,this}makeRotationFromQuaternion(e){return this.compose(x0,e,S0)}lookAt(e,t,n){let s=this.elements;return Cn.subVectors(e,t),Cn.lengthSq()===0&&(Cn.z=1),Cn.normalize(),Ti.crossVectors(n,Cn),Ti.lengthSq()===0&&(Math.abs(n.z)===1?Cn.x+=1e-4:Cn.z+=1e-4,Cn.normalize(),Ti.crossVectors(n,Cn)),Ti.normalize(),da.crossVectors(Cn,Ti),s[0]=Ti.x,s[4]=da.x,s[8]=Cn.x,s[1]=Ti.y,s[5]=da.y,s[9]=Cn.y,s[2]=Ti.z,s[6]=da.z,s[10]=Cn.z,this}multiply(e){return this.multiplyMatrices(this,e)}premultiply(e){return this.multiplyMatrices(e,this)}multiplyMatrices(e,t){let n=e.elements,s=t.elements,o=this.elements,l=n[0],h=n[4],d=n[8],f=n[12],g=n[1],y=n[5],m=n[9],S=n[13],T=n[2],P=n[6],b=n[10],_=n[14],U=n[3],z=n[7],R=n[11],I=n[15],L=s[0],B=s[4],w=s[8],D=s[12],O=s[1],q=s[5],Y=s[9],J=s[13],H=s[2],te=s[6],k=s[10],se=s[14],_e=s[3],ae=s[7],V=s[11],ge=s[15];return o[0]=l*L+h*O+d*H+f*_e,o[4]=l*B+h*q+d*te+f*ae,o[8]=l*w+h*Y+d*k+f*V,o[12]=l*D+h*J+d*se+f*ge,o[1]=g*L+y*O+m*H+S*_e,o[5]=g*B+y*q+m*te+S*ae,o[9]=g*w+y*Y+m*k+S*V,o[13]=g*D+y*J+m*se+S*ge,o[2]=T*L+P*O+b*H+_*_e,o[6]=T*B+P*q+b*te+_*ae,o[10]=T*w+P*Y+b*k+_*V,o[14]=T*D+P*J+b*se+_*ge,o[3]=U*L+z*O+R*H+I*_e,o[7]=U*B+z*q+R*te+I*ae,o[11]=U*w+z*Y+R*k+I*V,o[15]=U*D+z*J+R*se+I*ge,this}multiplyScalar(e){let t=this.elements;return t[0]*=e,t[4]*=e,t[8]*=e,t[12]*=e,t[1]*=e,t[5]*=e,t[9]*=e,t[13]*=e,t[2]*=e,t[6]*=e,t[10]*=e,t[14]*=e,t[3]*=e,t[7]*=e,t[11]*=e,t[15]*=e,this}determinant(){let e=this.elements,t=e[0],n=e[4],s=e[8],o=e[12],l=e[1],h=e[5],d=e[9],f=e[13],g=e[2],y=e[6],m=e[10],S=e[14],T=e[3],P=e[7],b=e[11],_=e[15],U=d*S-f*m,z=h*S-f*y,R=h*m-d*y,I=l*S-f*g,L=l*m-d*g,B=l*y-h*g;return t*(P*U-b*z+_*R)-n*(T*U-b*I+_*L)+s*(T*z-P*I+_*B)-o*(T*R-P*L+b*B)}determinantAffine(){let e=this.elements,t=e[0],n=e[4],s=e[8],o=e[1],l=e[5],h=e[9],d=e[2],f=e[6],g=e[10];return t*(l*g-h*f)-n*(o*g-h*d)+s*(o*f-l*d)}transpose(){let e=this.elements,t;return t=e[1],e[1]=e[4],e[4]=t,t=e[2],e[2]=e[8],e[8]=t,t=e[6],e[6]=e[9],e[9]=t,t=e[3],e[3]=e[12],e[12]=t,t=e[7],e[7]=e[13],e[13]=t,t=e[11],e[11]=e[14],e[14]=t,this}setPosition(e,t,n){let s=this.elements;return e.isVector3?(s[12]=e.x,s[13]=e.y,s[14]=e.z):(s[12]=e,s[13]=t,s[14]=n),this}invert(){let e=this.elements,t=e[0],n=e[1],s=e[2],o=e[3],l=e[4],h=e[5],d=e[6],f=e[7],g=e[8],y=e[9],m=e[10],S=e[11],T=e[12],P=e[13],b=e[14],_=e[15],U=t*h-n*l,z=t*d-s*l,R=t*f-o*l,I=n*d-s*h,L=n*f-o*h,B=s*f-o*d,w=g*P-y*T,D=g*b-m*T,O=g*_-S*T,q=y*b-m*P,Y=y*_-S*P,J=m*_-S*b,H=U*J-z*Y+R*q+I*O-L*D+B*w;if(H===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let te=1/H;return e[0]=(h*J-d*Y+f*q)*te,e[1]=(s*Y-n*J-o*q)*te,e[2]=(P*B-b*L+_*I)*te,e[3]=(m*L-y*B-S*I)*te,e[4]=(d*O-l*J-f*D)*te,e[5]=(t*J-s*O+o*D)*te,e[6]=(b*R-T*B-_*z)*te,e[7]=(g*B-m*R+S*z)*te,e[8]=(l*Y-h*O+f*w)*te,e[9]=(n*O-t*Y-o*w)*te,e[10]=(T*L-P*R+_*U)*te,e[11]=(y*R-g*L-S*U)*te,e[12]=(h*D-l*q-d*w)*te,e[13]=(t*q-n*D+s*w)*te,e[14]=(P*z-T*I-b*U)*te,e[15]=(g*I-y*z+m*U)*te,this}scale(e){let t=this.elements,n=e.x,s=e.y,o=e.z;return t[0]*=n,t[4]*=s,t[8]*=o,t[1]*=n,t[5]*=s,t[9]*=o,t[2]*=n,t[6]*=s,t[10]*=o,t[3]*=n,t[7]*=s,t[11]*=o,this}getMaxScaleOnAxis(){let e=this.elements,t=e[0]*e[0]+e[1]*e[1]+e[2]*e[2],n=e[4]*e[4]+e[5]*e[5]+e[6]*e[6],s=e[8]*e[8]+e[9]*e[9]+e[10]*e[10];return Math.sqrt(Math.max(t,n,s))}makeTranslation(e,t,n){return e.isVector3?this.set(1,0,0,e.x,0,1,0,e.y,0,0,1,e.z,0,0,0,1):this.set(1,0,0,e,0,1,0,t,0,0,1,n,0,0,0,1),this}makeRotationX(e){let t=Math.cos(e),n=Math.sin(e);return this.set(1,0,0,0,0,t,-n,0,0,n,t,0,0,0,0,1),this}makeRotationY(e){let t=Math.cos(e),n=Math.sin(e);return this.set(t,0,n,0,0,1,0,0,-n,0,t,0,0,0,0,1),this}makeRotationZ(e){let t=Math.cos(e),n=Math.sin(e);return this.set(t,-n,0,0,n,t,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(e,t){let n=Math.cos(t),s=Math.sin(t),o=1-n,l=e.x,h=e.y,d=e.z,f=o*l,g=o*h;return this.set(f*l+n,f*h-s*d,f*d+s*h,0,f*h+s*d,g*h+n,g*d-s*l,0,f*d-s*h,g*d+s*l,o*d*d+n,0,0,0,0,1),this}makeScale(e,t,n){return this.set(e,0,0,0,0,t,0,0,0,0,n,0,0,0,0,1),this}makeShear(e,t,n,s,o,l){return this.set(1,n,o,0,e,1,l,0,t,s,1,0,0,0,0,1),this}compose(e,t,n){let s=this.elements,o=t._x,l=t._y,h=t._z,d=t._w,f=o+o,g=l+l,y=h+h,m=o*f,S=o*g,T=o*y,P=l*g,b=l*y,_=h*y,U=d*f,z=d*g,R=d*y,I=n.x,L=n.y,B=n.z;return s[0]=(1-(P+_))*I,s[1]=(S+R)*I,s[2]=(T-z)*I,s[3]=0,s[4]=(S-R)*L,s[5]=(1-(m+_))*L,s[6]=(b+U)*L,s[7]=0,s[8]=(T+z)*B,s[9]=(b-U)*B,s[10]=(1-(m+P))*B,s[11]=0,s[12]=e.x,s[13]=e.y,s[14]=e.z,s[15]=1,this}decompose(e,t,n){let s=this.elements;e.x=s[12],e.y=s[13],e.z=s[14];let o=this.determinantAffine();if(o===0)return n.set(1,1,1),t.identity(),this;let l=gr.set(s[0],s[1],s[2]).length(),h=gr.set(s[4],s[5],s[6]).length(),d=gr.set(s[8],s[9],s[10]).length();o<0&&(l=-l),$n.copy(this);let f=1/l,g=1/h,y=1/d;return $n.elements[0]*=f,$n.elements[1]*=f,$n.elements[2]*=f,$n.elements[4]*=g,$n.elements[5]*=g,$n.elements[6]*=g,$n.elements[8]*=y,$n.elements[9]*=y,$n.elements[10]*=y,t.setFromRotationMatrix($n),n.x=l,n.y=h,n.z=d,this}makePerspective(e,t,n,s,o,l,h=Yn,d=!1){let f=this.elements,g=2*o/(t-e),y=2*o/(n-s),m=(t+e)/(t-e),S=(n+s)/(n-s),T,P;if(d)T=o/(l-o),P=l*o/(l-o);else if(h===Yn)T=-(l+o)/(l-o),P=-2*l*o/(l-o);else if(h===Ir)T=-l/(l-o),P=-l*o/(l-o);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+h);return f[0]=g,f[4]=0,f[8]=m,f[12]=0,f[1]=0,f[5]=y,f[9]=S,f[13]=0,f[2]=0,f[6]=0,f[10]=T,f[14]=P,f[3]=0,f[7]=0,f[11]=-1,f[15]=0,this}makeOrthographic(e,t,n,s,o,l,h=Yn,d=!1){let f=this.elements,g=2/(t-e),y=2/(n-s),m=-(t+e)/(t-e),S=-(n+s)/(n-s),T,P;if(d)T=1/(l-o),P=l/(l-o);else if(h===Yn)T=-2/(l-o),P=-(l+o)/(l-o);else if(h===Ir)T=-1/(l-o),P=-o/(l-o);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+h);return f[0]=g,f[4]=0,f[8]=0,f[12]=m,f[1]=0,f[5]=y,f[9]=0,f[13]=S,f[2]=0,f[6]=0,f[10]=T,f[14]=P,f[3]=0,f[7]=0,f[11]=0,f[15]=1,this}equals(e){let t=this.elements,n=e.elements;for(let s=0;s<16;s++)if(t[s]!==n[s])return!1;return!0}fromArray(e,t=0){for(let n=0;n<16;n++)this.elements[n]=e[n+t];return this}toArray(e=[],t=0){let n=this.elements;return e[t]=n[0],e[t+1]=n[1],e[t+2]=n[2],e[t+3]=n[3],e[t+4]=n[4],e[t+5]=n[5],e[t+6]=n[6],e[t+7]=n[7],e[t+8]=n[8],e[t+9]=n[9],e[t+10]=n[10],e[t+11]=n[11],e[t+12]=n[12],e[t+13]=n[13],e[t+14]=n[14],e[t+15]=n[15],e}},gr=new j,$n=new Ot,x0=new j(0,0,0),S0=new j(1,1,1),Ti=new j,da=new j,Cn=new j,Yh=new Ot,Zh=new In,xi=class i{constructor(e=0,t=0,n=0,s=i.DEFAULT_ORDER){this.isEuler=!0,this._x=e,this._y=t,this._z=n,this._order=s}get x(){return this._x}set x(e){this._x=e,this._onChangeCallback()}get y(){return this._y}set y(e){this._y=e,this._onChangeCallback()}get z(){return this._z}set z(e){this._z=e,this._onChangeCallback()}get order(){return this._order}set order(e){this._order=e,this._onChangeCallback()}set(e,t,n,s=this._order){return this._x=e,this._y=t,this._z=n,this._order=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(e){return this._x=e._x,this._y=e._y,this._z=e._z,this._order=e._order,this._onChangeCallback(),this}setFromRotationMatrix(e,t=this._order,n=!0){let s=e.elements,o=s[0],l=s[4],h=s[8],d=s[1],f=s[5],g=s[9],y=s[2],m=s[6],S=s[10];switch(t){case"XYZ":this._y=Math.asin(_t(h,-1,1)),Math.abs(h)<.9999999?(this._x=Math.atan2(-g,S),this._z=Math.atan2(-l,o)):(this._x=Math.atan2(m,f),this._z=0);break;case"YXZ":this._x=Math.asin(-_t(g,-1,1)),Math.abs(g)<.9999999?(this._y=Math.atan2(h,S),this._z=Math.atan2(d,f)):(this._y=Math.atan2(-y,o),this._z=0);break;case"ZXY":this._x=Math.asin(_t(m,-1,1)),Math.abs(m)<.9999999?(this._y=Math.atan2(-y,S),this._z=Math.atan2(-l,f)):(this._y=0,this._z=Math.atan2(d,o));break;case"ZYX":this._y=Math.asin(-_t(y,-1,1)),Math.abs(y)<.9999999?(this._x=Math.atan2(m,S),this._z=Math.atan2(d,o)):(this._x=0,this._z=Math.atan2(-l,f));break;case"YZX":this._z=Math.asin(_t(d,-1,1)),Math.abs(d)<.9999999?(this._x=Math.atan2(-g,f),this._y=Math.atan2(-y,o)):(this._x=0,this._y=Math.atan2(h,S));break;case"XZY":this._z=Math.asin(-_t(l,-1,1)),Math.abs(l)<.9999999?(this._x=Math.atan2(m,f),this._y=Math.atan2(h,o)):(this._x=Math.atan2(-g,S),this._y=0);break;default:et("Euler: .setFromRotationMatrix() encountered an unknown order: "+t)}return this._order=t,n===!0&&this._onChangeCallback(),this}setFromQuaternion(e,t,n){return Yh.makeRotationFromQuaternion(e),this.setFromRotationMatrix(Yh,t,n)}setFromVector3(e,t=this._order){return this.set(e.x,e.y,e.z,t)}reorder(e){return Zh.setFromEuler(this),this.setFromQuaternion(Zh,e)}equals(e){return e._x===this._x&&e._y===this._y&&e._z===this._z&&e._order===this._order}fromArray(e){return this._x=e[0],this._y=e[1],this._z=e[2],e[3]!==void 0&&(this._order=e[3]),this._onChangeCallback(),this}toArray(e=[],t=0){return e[t]=this._x,e[t+1]=this._y,e[t+2]=this._z,e[t+3]=this._order,e}_onChange(e){return this._onChangeCallback=e,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};xi.DEFAULT_ORDER="XYZ";var Nr=class{constructor(){this.mask=1}set(e){this.mask=(1<<e|0)>>>0}enable(e){this.mask|=1<<e|0}enableAll(){this.mask=-1}toggle(e){this.mask^=1<<e|0}disable(e){this.mask&=~(1<<e|0)}disableAll(){this.mask=0}test(e){return(this.mask&e.mask)!==0}isEnabled(e){return(this.mask&(1<<e|0))!==0}},b0=0,Jh=new j,_r=new In,pi=new Ot,fa=new j,is=new j,M0=new j,E0=new In,Kh=new j(1,0,0),Qh=new j(0,1,0),eu=new j(0,0,1),tu={type:"added"},w0={type:"removed"},vr={type:"childadded",child:null},Ol={type:"childremoved",child:null},on=class i extends Zn{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:b0++}),this.uuid=jr(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=i.DEFAULT_UP.clone();let e=new j,t=new xi,n=new In,s=new j(1,1,1);function o(){n.setFromEuler(t,!1)}function l(){t.setFromQuaternion(n,void 0,!1)}t._onChange(o),n._onChange(l),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:e},rotation:{configurable:!0,enumerable:!0,value:t},quaternion:{configurable:!0,enumerable:!0,value:n},scale:{configurable:!0,enumerable:!0,value:s},modelViewMatrix:{value:new Ot},normalMatrix:{value:new at}}),this.matrix=new Ot,this.matrixWorld=new Ot,this.matrixAutoUpdate=i.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=i.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new Nr,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.static=!1,this.userData={},this.pivot=null}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(e){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(e),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(e){return this.quaternion.premultiply(e),this}setRotationFromAxisAngle(e,t){this.quaternion.setFromAxisAngle(e,t)}setRotationFromEuler(e){this.quaternion.setFromEuler(e,!0)}setRotationFromMatrix(e){this.quaternion.setFromRotationMatrix(e)}setRotationFromQuaternion(e){this.quaternion.copy(e)}rotateOnAxis(e,t){return _r.setFromAxisAngle(e,t),this.quaternion.multiply(_r),this}rotateOnWorldAxis(e,t){return _r.setFromAxisAngle(e,t),this.quaternion.premultiply(_r),this}rotateX(e){return this.rotateOnAxis(Kh,e)}rotateY(e){return this.rotateOnAxis(Qh,e)}rotateZ(e){return this.rotateOnAxis(eu,e)}translateOnAxis(e,t){return Jh.copy(e).applyQuaternion(this.quaternion),this.position.add(Jh.multiplyScalar(t)),this}translateX(e){return this.translateOnAxis(Kh,e)}translateY(e){return this.translateOnAxis(Qh,e)}translateZ(e){return this.translateOnAxis(eu,e)}localToWorld(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(this.matrixWorld)}worldToLocal(e){return this.updateWorldMatrix(!0,!1),e.applyMatrix4(pi.copy(this.matrixWorld).invert())}lookAt(e,t,n){e.isVector3?fa.copy(e):fa.set(e,t,n);let s=this.parent;this.updateWorldMatrix(!0,!1),is.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?pi.lookAt(is,fa,this.up):pi.lookAt(fa,is,this.up),this.quaternion.setFromRotationMatrix(pi),s&&(pi.extractRotation(s.matrixWorld),_r.setFromRotationMatrix(pi),this.quaternion.premultiply(_r.invert()))}add(e){if(arguments.length>1){for(let t=0;t<arguments.length;t++)this.add(arguments[t]);return this}return e===this?(it("Object3D.add: object can't be added as a child of itself.",e),this):(e&&e.isObject3D?(e.removeFromParent(),e.parent=this,this.children.push(e),e.dispatchEvent(tu),vr.child=e,this.dispatchEvent(vr),vr.child=null):it("Object3D.add: object not an instance of THREE.Object3D.",e),this)}remove(e){if(arguments.length>1){for(let n=0;n<arguments.length;n++)this.remove(arguments[n]);return this}let t=this.children.indexOf(e);return t!==-1&&(e.parent=null,this.children.splice(t,1),e.dispatchEvent(w0),Ol.child=e,this.dispatchEvent(Ol),Ol.child=null),this}removeFromParent(){let e=this.parent;return e!==null&&e.remove(this),this}clear(){return this.remove(...this.children)}attach(e){return this.updateWorldMatrix(!0,!1),pi.copy(this.matrixWorld).invert(),e.parent!==null&&(e.parent.updateWorldMatrix(!0,!1),pi.multiply(e.parent.matrixWorld)),e.applyMatrix4(pi),e.removeFromParent(),e.parent=this,this.children.push(e),e.updateWorldMatrix(!1,!0),e.dispatchEvent(tu),vr.child=e,this.dispatchEvent(vr),vr.child=null,this}getObjectById(e){return this.getObjectByProperty("id",e)}getObjectByName(e){return this.getObjectByProperty("name",e)}getObjectByProperty(e,t){if(this[e]===t)return this;for(let n=0,s=this.children.length;n<s;n++){let l=this.children[n].getObjectByProperty(e,t);if(l!==void 0)return l}}getObjectsByProperty(e,t,n=[]){this[e]===t&&n.push(this);let s=this.children;for(let o=0,l=s.length;o<l;o++)s[o].getObjectsByProperty(e,t,n);return n}getWorldPosition(e){return this.updateWorldMatrix(!0,!1),e.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(is,e,M0),e}getWorldScale(e){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(is,E0,e),e}getWorldDirection(e){this.updateWorldMatrix(!0,!1);let t=this.matrixWorld.elements;return e.set(t[8],t[9],t[10]).normalize()}raycast(){}intersectsFrustum(){}traverse(e){e(this);let t=this.children;for(let n=0,s=t.length;n<s;n++)t[n].traverse(e)}traverseVisible(e){if(this.visible===!1)return;e(this);let t=this.children;for(let n=0,s=t.length;n<s;n++)t[n].traverseVisible(e)}traverseAncestors(e){let t=this.parent;t!==null&&(e(t),t.traverseAncestors(e))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale);let e=this.pivot;if(e!==null){let t=e.x,n=e.y,s=e.z,o=this.matrix.elements;o[12]+=t-o[0]*t-o[4]*n-o[8]*s,o[13]+=n-o[1]*t-o[5]*n-o[9]*s,o[14]+=s-o[2]*t-o[6]*n-o[10]*s}this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(e){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||e)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,e=!0);let t=this.children;for(let n=0,s=t.length;n<s;n++)t[n].updateMatrixWorld(e)}updateWorldMatrix(e,t,n=!1){let s=this.parent;if(e===!0&&s!==null&&s.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||n)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,n=!0),t===!0){let o=this.children;for(let l=0,h=o.length;l<h;l++)o[l].updateWorldMatrix(!1,!0,n)}}toJSON(e){let t=e===void 0||typeof e=="string",n={};t&&(e={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},n.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let s={};s.uuid=this.uuid,s.type=this.type,s.name=this.name,s.castShadow=this.castShadow,s.receiveShadow=this.receiveShadow,s.visible=this.visible,s.frustumCulled=this.frustumCulled,s.renderOrder=this.renderOrder,s.static=this.static,s.matrixAutoUpdate=this.matrixAutoUpdate,Object.keys(this.userData).length>0&&(s.userData=this.userData),s.layers=this.layers.mask,s.matrix=this.matrix.toArray(),s.up=this.up.toArray(),this.pivot!==null&&(s.pivot=this.pivot.toArray()),this.morphTargetDictionary!==void 0&&(s.morphTargetDictionary=Object.assign({},this.morphTargetDictionary)),this.morphTargetInfluences!==void 0&&(s.morphTargetInfluences=this.morphTargetInfluences.slice()),this.isInstancedMesh&&(s.type="InstancedMesh",s.count=this.count,s.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(s.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(s.type="BatchedMesh",s.perObjectFrustumCulled=this.perObjectFrustumCulled,s.sortObjects=this.sortObjects,s.drawRanges=this._drawRanges,s.reservedRanges=this._reservedRanges,s.geometryInfo=this._geometryInfo.map(h=>({...h,boundingBox:h.boundingBox?h.boundingBox.toJSON():void 0,boundingSphere:h.boundingSphere?h.boundingSphere.toJSON():void 0})),s.instanceInfo=this._instanceInfo.map(h=>({...h})),s.availableInstanceIds=this._availableInstanceIds.slice(),s.availableGeometryIds=this._availableGeometryIds.slice(),s.nextIndexStart=this._nextIndexStart,s.nextVertexStart=this._nextVertexStart,s.geometryCount=this._geometryCount,s.maxInstanceCount=this._maxInstanceCount,s.maxVertexCount=this._maxVertexCount,s.maxIndexCount=this._maxIndexCount,s.geometryInitialized=this._geometryInitialized,s.matricesTexture=this._matricesTexture.toJSON(e),s.indirectTexture=this._indirectTexture.toJSON(e),this._colorsTexture!==null&&(s.colorsTexture=this._colorsTexture.toJSON(e)),this.boundingSphere!==null&&(s.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(s.boundingBox=this.boundingBox.toJSON()));function o(h,d){return h[d.uuid]===void 0&&(h[d.uuid]=d.toJSON(e)),d.uuid}if(this.isScene)this.background&&(this.background.isColor?s.background=this.background.toJSON():this.background.isTexture&&(s.background=this.background.toJSON(e).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(s.environment=this.environment.toJSON(e).uuid);else if(this.isMesh||this.isLine||this.isPoints){s.geometry=o(e.geometries,this.geometry);let h=this.geometry.parameters;if(h!==void 0&&h.shapes!==void 0){let d=h.shapes;if(Array.isArray(d))for(let f=0,g=d.length;f<g;f++){let y=d[f];o(e.shapes,y)}else o(e.shapes,d)}}if(this.isSkinnedMesh&&(s.bindMode=this.bindMode,s.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(o(e.skeletons,this.skeleton),s.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let h=[];for(let d=0,f=this.material.length;d<f;d++)h.push(o(e.materials,this.material[d]));s.material=h}else s.material=o(e.materials,this.material);if(this.children.length>0){s.children=[];for(let h=0;h<this.children.length;h++)s.children.push(this.children[h].toJSON(e).object)}if(this.animations.length>0){s.animations=[];for(let h=0;h<this.animations.length;h++){let d=this.animations[h];s.animations.push(o(e.animations,d))}}if(t){let h=l(e.geometries),d=l(e.materials),f=l(e.textures),g=l(e.images),y=l(e.shapes),m=l(e.skeletons),S=l(e.animations),T=l(e.nodes);h.length>0&&(n.geometries=h),d.length>0&&(n.materials=d),f.length>0&&(n.textures=f),g.length>0&&(n.images=g),y.length>0&&(n.shapes=y),m.length>0&&(n.skeletons=m),S.length>0&&(n.animations=S),T.length>0&&(n.nodes=T)}return n.object=s,n;function l(h){let d=[];for(let f in h){let g=h[f];delete g.metadata,d.push(g)}return d}}clone(e){return new this.constructor().copy(this,e)}copy(e,t=!0){if(this.name=e.name,this.up.copy(e.up),this.position.copy(e.position),this.rotation.order=e.rotation.order,this.quaternion.copy(e.quaternion),this.scale.copy(e.scale),this.pivot=e.pivot!==null?e.pivot.clone():null,this.matrix.copy(e.matrix),this.matrixWorld.copy(e.matrixWorld),this.matrixAutoUpdate=e.matrixAutoUpdate,this.matrixWorldAutoUpdate=e.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=e.matrixWorldNeedsUpdate,this.layers.mask=e.layers.mask,this.visible=e.visible,this.castShadow=e.castShadow,this.receiveShadow=e.receiveShadow,this.frustumCulled=e.frustumCulled,this.renderOrder=e.renderOrder,this.static=e.static,this.animations=e.animations.slice(),this.userData=JSON.parse(JSON.stringify(e.userData)),t===!0)for(let n=0;n<e.children.length;n++){let s=e.children[n];this.add(s.clone())}return this}dispose(){this.dispatchEvent({type:"dispose"})}};on.DEFAULT_UP=new j(0,1,0);on.DEFAULT_MATRIX_AUTO_UPDATE=!0;on.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var tr=class extends on{constructor(){super(),this.isGroup=!0,this.type="Group"}},T0={type:"move"},Ur=class{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new tr,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new tr,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new j,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new j),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new tr,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new j,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new j,this._grip.eventsEnabled=!1),this._grip}dispatchEvent(e){return this._targetRay!==null&&this._targetRay.dispatchEvent(e),this._grip!==null&&this._grip.dispatchEvent(e),this._hand!==null&&this._hand.dispatchEvent(e),this}connect(e){if(e&&e.hand){let t=this._hand;if(t)for(let n of e.hand.values())this._getHandJoint(t,n)}return this.dispatchEvent({type:"connected",data:e}),this}disconnect(e){return this.dispatchEvent({type:"disconnected",data:e}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(e,t,n){let s=null,o=null,l=null,h=this._targetRay,d=this._grip,f=this._hand;if(e&&t.session.visibilityState!=="visible-blurred"){if(f&&e.hand){l=!0;for(let P of e.hand.values()){let b=t.getJointPose(P,n),_=this._getHandJoint(f,P);b!==null&&(_.matrix.fromArray(b.transform.matrix),_.matrix.decompose(_.position,_.rotation,_.scale),_.matrixWorldNeedsUpdate=!0,_.jointRadius=b.radius),_.visible=b!==null}let g=f.joints["index-finger-tip"],y=f.joints["thumb-tip"],m=g.position.distanceTo(y.position),S=.02,T=.005;f.inputState.pinching&&m>S+T?(f.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:e.handedness,target:this})):!f.inputState.pinching&&m<=S-T&&(f.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:e.handedness,target:this}))}else d!==null&&e.gripSpace&&(o=t.getPose(e.gripSpace,n),o!==null&&(d.matrix.fromArray(o.transform.matrix),d.matrix.decompose(d.position,d.rotation,d.scale),d.matrixWorldNeedsUpdate=!0,o.linearVelocity?(d.hasLinearVelocity=!0,d.linearVelocity.copy(o.linearVelocity)):d.hasLinearVelocity=!1,o.angularVelocity?(d.hasAngularVelocity=!0,d.angularVelocity.copy(o.angularVelocity)):d.hasAngularVelocity=!1,d.eventsEnabled&&d.dispatchEvent({type:"gripUpdated",data:e,target:this})));h!==null&&(s=t.getPose(e.targetRaySpace,n),s===null&&o!==null&&(s=o),s!==null&&(h.matrix.fromArray(s.transform.matrix),h.matrix.decompose(h.position,h.rotation,h.scale),h.matrixWorldNeedsUpdate=!0,s.linearVelocity?(h.hasLinearVelocity=!0,h.linearVelocity.copy(s.linearVelocity)):h.hasLinearVelocity=!1,s.angularVelocity?(h.hasAngularVelocity=!0,h.angularVelocity.copy(s.angularVelocity)):h.hasAngularVelocity=!1,this.dispatchEvent(T0)))}return h!==null&&(h.visible=s!==null),d!==null&&(d.visible=o!==null),f!==null&&(f.visible=l!==null),this}_getHandJoint(e,t){if(e.joints[t.jointName]===void 0){let n=new tr;n.matrixAutoUpdate=!1,n.visible=!1,e.joints[t.jointName]=n,e.add(n)}return e.joints[t.jointName]}},id={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},Ai={h:0,s:0,l:0},pa={h:0,s:0,l:0};function Bl(i,e,t){return t<0&&(t+=1),t>1&&(t-=1),t<1/6?i+(e-i)*6*t:t<1/2?e:t<2/3?i+(e-i)*6*(2/3-t):i}var ht=class{constructor(e,t,n){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(e,t,n)}set(e,t,n){if(t===void 0&&n===void 0){let s=e;s&&s.isColor?this.copy(s):typeof s=="number"?this.setHex(s):typeof s=="string"&&this.setStyle(s)}else this.setRGB(e,t,n);return this}setScalar(e){return this.r=e,this.g=e,this.b=e,this}setHex(e,t=dn){return e=Math.floor(e),this.r=(e>>16&255)/255,this.g=(e>>8&255)/255,this.b=(e&255)/255,xt.colorSpaceToWorking(this,t),this}setRGB(e,t,n,s=xt.workingColorSpace){return this.r=e,this.g=t,this.b=n,xt.colorSpaceToWorking(this,s),this}setHSL(e,t,n,s=xt.workingColorSpace){if(e=Lc(e,1),t=_t(t,0,1),n=_t(n,0,1),t===0)this.r=this.g=this.b=n;else{let o=n<=.5?n*(1+t):n+t-n*t,l=2*n-o;this.r=Bl(l,o,e+1/3),this.g=Bl(l,o,e),this.b=Bl(l,o,e-1/3)}return xt.colorSpaceToWorking(this,s),this}setStyle(e,t=dn){function n(o){o!==void 0&&parseFloat(o)<1&&et("Color: Alpha component of "+e+" will be ignored.")}let s;if(s=/^(\w+)\(([^\)]*)\)/.exec(e)){let o,l=s[1],h=s[2];switch(l){case"rgb":case"rgba":if(o=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return n(o[4]),this.setRGB(Math.min(255,parseInt(o[1],10))/255,Math.min(255,parseInt(o[2],10))/255,Math.min(255,parseInt(o[3],10))/255,t);if(o=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return n(o[4]),this.setRGB(Math.min(100,parseInt(o[1],10))/100,Math.min(100,parseInt(o[2],10))/100,Math.min(100,parseInt(o[3],10))/100,t);break;case"hsl":case"hsla":if(o=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(h))return n(o[4]),this.setHSL(parseFloat(o[1])/360,parseFloat(o[2])/100,parseFloat(o[3])/100,t);break;default:et("Color: Unknown color model "+e)}}else if(s=/^\#([A-Fa-f\d]+)$/.exec(e)){let o=s[1],l=o.length;if(l===3)return this.setRGB(parseInt(o.charAt(0),16)/15,parseInt(o.charAt(1),16)/15,parseInt(o.charAt(2),16)/15,t);if(l===6)return this.setHex(parseInt(o,16),t);et("Color: Invalid hex color "+e)}else if(e&&e.length>0)return this.setColorName(e,t);return this}setColorName(e,t=dn){let n=id[e.toLowerCase()];return n!==void 0?this.setHex(n,t):et("Color: Unknown color "+e),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(e){return this.r=e.r,this.g=e.g,this.b=e.b,this}copySRGBToLinear(e){return this.r=yi(e.r),this.g=yi(e.g),this.b=yi(e.b),this}copyLinearToSRGB(e){return this.r=Rr(e.r),this.g=Rr(e.g),this.b=Rr(e.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(e=dn){return xt.workingToColorSpace(un.copy(this),e),Math.round(_t(un.r*255,0,255))*65536+Math.round(_t(un.g*255,0,255))*256+Math.round(_t(un.b*255,0,255))}getHexString(e=dn){return("000000"+this.getHex(e).toString(16)).slice(-6)}getHSL(e,t=xt.workingColorSpace){xt.workingToColorSpace(un.copy(this),t);let n=un.r,s=un.g,o=un.b,l=Math.max(n,s,o),h=Math.min(n,s,o),d,f,g=(h+l)/2;if(h===l)d=0,f=0;else{let y=l-h;switch(f=g<=.5?y/(l+h):y/(2-l-h),l){case n:d=(s-o)/y+(s<o?6:0);break;case s:d=(o-n)/y+2;break;case o:d=(n-s)/y+4;break}d/=6}return e.h=d,e.s=f,e.l=g,e}getRGB(e,t=xt.workingColorSpace){return xt.workingToColorSpace(un.copy(this),t),e.r=un.r,e.g=un.g,e.b=un.b,e}getStyle(e=dn){xt.workingToColorSpace(un.copy(this),e);let t=un.r,n=un.g,s=un.b;return e!==dn?`color(${e} ${t.toFixed(3)} ${n.toFixed(3)} ${s.toFixed(3)})`:`rgb(${Math.round(t*255)},${Math.round(n*255)},${Math.round(s*255)})`}offsetHSL(e,t,n){return this.getHSL(Ai),this.setHSL(Ai.h+e,Ai.s+t,Ai.l+n)}add(e){return this.r+=e.r,this.g+=e.g,this.b+=e.b,this}addColors(e,t){return this.r=e.r+t.r,this.g=e.g+t.g,this.b=e.b+t.b,this}addScalar(e){return this.r+=e,this.g+=e,this.b+=e,this}sub(e){return this.r=Math.max(0,this.r-e.r),this.g=Math.max(0,this.g-e.g),this.b=Math.max(0,this.b-e.b),this}multiply(e){return this.r*=e.r,this.g*=e.g,this.b*=e.b,this}multiplyScalar(e){return this.r*=e,this.g*=e,this.b*=e,this}lerp(e,t){return this.r+=(e.r-this.r)*t,this.g+=(e.g-this.g)*t,this.b+=(e.b-this.b)*t,this}lerpColors(e,t,n){return this.r=e.r+(t.r-e.r)*n,this.g=e.g+(t.g-e.g)*n,this.b=e.b+(t.b-e.b)*n,this}lerpHSL(e,t){this.getHSL(Ai),e.getHSL(pa);let n=cs(Ai.h,pa.h,t),s=cs(Ai.s,pa.s,t),o=cs(Ai.l,pa.l,t);return this.setHSL(n,s,o),this}setFromVector3(e){return this.r=e.x,this.g=e.y,this.b=e.z,this}applyMatrix3(e){let t=this.r,n=this.g,s=this.b,o=e.elements;return this.r=o[0]*t+o[3]*n+o[6]*s,this.g=o[1]*t+o[4]*n+o[7]*s,this.b=o[2]*t+o[5]*n+o[8]*s,this}equals(e){return e.r===this.r&&e.g===this.g&&e.b===this.b}fromArray(e,t=0){return this.r=e[t],this.g=e[t+1],this.b=e[t+2],this}toArray(e=[],t=0){return e[t]=this.r,e[t+1]=this.g,e[t+2]=this.b,e}fromBufferAttribute(e,t){return this.r=e.getX(t),this.g=e.getY(t),this.b=e.getZ(t),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},un=new ht;ht.NAMES=id;var ms=class extends on{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new xi,this.environmentIntensity=1,this.environmentRotation=new xi,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(e,t){return super.copy(e,t),e.background!==null&&(this.background=e.background.clone()),e.environment!==null&&(this.environment=e.environment.clone()),e.fog!==null&&(this.fog=e.fog.clone()),this.backgroundBlurriness=e.backgroundBlurriness,this.backgroundIntensity=e.backgroundIntensity,this.backgroundRotation.copy(e.backgroundRotation),this.environmentIntensity=e.environmentIntensity,this.environmentRotation.copy(e.environmentRotation),e.overrideMaterial!==null&&(this.overrideMaterial=e.overrideMaterial.clone()),this.matrixAutoUpdate=e.matrixAutoUpdate,this}toJSON(e){let t=super.toJSON(e);return this.fog!==null&&(t.object.fog=this.fog.toJSON()),t.object.backgroundBlurriness=this.backgroundBlurriness,t.object.backgroundIntensity=this.backgroundIntensity,t.object.backgroundRotation=this.backgroundRotation.toArray(),t.object.environmentIntensity=this.environmentIntensity,t.object.environmentRotation=this.environmentRotation.toArray(),t}},jn=new j,mi=new j,kl=new j,gi=new j,yr=new j,xr=new j,nu=new j,zl=new j,Vl=new j,Gl=new j,Hl=new Ht,Wl=new Ht,Xl=new Ht,Ii=class i{constructor(e=new j,t=new j,n=new j){this.a=e,this.b=t,this.c=n}static getNormal(e,t,n,s){s.subVectors(n,t),jn.subVectors(e,t),s.cross(jn);let o=s.lengthSq();return o>0?s.multiplyScalar(1/Math.sqrt(o)):s.set(0,0,0)}static getBarycoord(e,t,n,s,o){jn.subVectors(s,t),mi.subVectors(n,t),kl.subVectors(e,t);let l=jn.dot(jn),h=jn.dot(mi),d=jn.dot(kl),f=mi.dot(mi),g=mi.dot(kl),y=l*f-h*h;if(y===0)return o.set(0,0,0),null;let m=1/y,S=(f*d-h*g)*m,T=(l*g-h*d)*m;return o.set(1-S-T,T,S)}static containsPoint(e,t,n,s){return this.getBarycoord(e,t,n,s,gi)===null?!1:gi.x>=0&&gi.y>=0&&gi.x+gi.y<=1}static getInterpolation(e,t,n,s,o,l,h,d){return this.getBarycoord(e,t,n,s,gi)===null?(d.x=0,d.y=0,"z"in d&&(d.z=0),"w"in d&&(d.w=0),null):(d.setScalar(0),d.addScaledVector(o,gi.x),d.addScaledVector(l,gi.y),d.addScaledVector(h,gi.z),d)}static getInterpolatedAttribute(e,t,n,s,o,l){return Hl.setScalar(0),Wl.setScalar(0),Xl.setScalar(0),Hl.fromBufferAttribute(e,t),Wl.fromBufferAttribute(e,n),Xl.fromBufferAttribute(e,s),l.setScalar(0),l.addScaledVector(Hl,o.x),l.addScaledVector(Wl,o.y),l.addScaledVector(Xl,o.z),l}static isFrontFacing(e,t,n,s){return jn.subVectors(n,t),mi.subVectors(e,t),jn.cross(mi).dot(s)<0}set(e,t,n){return this.a.copy(e),this.b.copy(t),this.c.copy(n),this}setFromPointsAndIndices(e,t,n,s){return this.a.copy(e[t]),this.b.copy(e[n]),this.c.copy(e[s]),this}setFromAttributeAndIndices(e,t,n,s){return this.a.fromBufferAttribute(e,t),this.b.fromBufferAttribute(e,n),this.c.fromBufferAttribute(e,s),this}clone(){return new this.constructor().copy(this)}copy(e){return this.a.copy(e.a),this.b.copy(e.b),this.c.copy(e.c),this}getArea(){return jn.subVectors(this.c,this.b),mi.subVectors(this.a,this.b),jn.cross(mi).length()*.5}getMidpoint(e){return e.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(e){return i.getNormal(this.a,this.b,this.c,e)}getPlane(e){return e.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(e,t){return i.getBarycoord(e,this.a,this.b,this.c,t)}getInterpolation(e,t,n,s,o){return i.getInterpolation(e,this.a,this.b,this.c,t,n,s,o)}containsPoint(e){return i.containsPoint(e,this.a,this.b,this.c)}isFrontFacing(e){return i.isFrontFacing(this.a,this.b,this.c,e)}intersectsBox(e){return e.intersectsTriangle(this)}closestPointToPoint(e,t){let n=this.a,s=this.b,o=this.c,l,h;yr.subVectors(s,n),xr.subVectors(o,n),zl.subVectors(e,n);let d=yr.dot(zl),f=xr.dot(zl);if(d<=0&&f<=0)return t.copy(n);Vl.subVectors(e,s);let g=yr.dot(Vl),y=xr.dot(Vl);if(g>=0&&y<=g)return t.copy(s);let m=d*y-g*f;if(m<=0&&d>=0&&g<=0)return l=d/(d-g),t.copy(n).addScaledVector(yr,l);Gl.subVectors(e,o);let S=yr.dot(Gl),T=xr.dot(Gl);if(T>=0&&S<=T)return t.copy(o);let P=S*f-d*T;if(P<=0&&f>=0&&T<=0)return h=f/(f-T),t.copy(n).addScaledVector(xr,h);let b=g*T-S*y;if(b<=0&&y-g>=0&&S-T>=0)return nu.subVectors(o,s),h=(y-g)/(y-g+(S-T)),t.copy(s).addScaledVector(nu,h);let _=1/(b+P+m);return l=P*_,h=m*_,t.copy(n).addScaledVector(yr,l).addScaledVector(xr,h)}equals(e){return e.a.equals(this.a)&&e.b.equals(this.b)&&e.c.equals(this.c)}},oi=class{constructor(e=new j(1/0,1/0,1/0),t=new j(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=e,this.max=t}set(e,t){return this.min.copy(e),this.max.copy(t),this}setFromArray(e){this.makeEmpty();for(let t=0,n=e.length;t<n;t+=3)this.expandByPoint(qn.fromArray(e,t));return this}setFromBufferAttribute(e){this.makeEmpty();for(let t=0,n=e.count;t<n;t++)this.expandByPoint(qn.fromBufferAttribute(e,t));return this}setFromPoints(e){this.makeEmpty();for(let t=0,n=e.length;t<n;t++)this.expandByPoint(e[t]);return this}setFromCenterAndSize(e,t){let n=qn.copy(t).multiplyScalar(.5);return this.min.copy(e).sub(n),this.max.copy(e).add(n),this}setFromObject(e,t=!1){return this.makeEmpty(),this.expandByObject(e,t)}clone(){return new this.constructor().copy(this)}copy(e){return this.min.copy(e.min),this.max.copy(e.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(e){return this.isEmpty()?e.set(0,0,0):e.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(e){return this.isEmpty()?e.set(0,0,0):e.subVectors(this.max,this.min)}expandByPoint(e){return this.min.min(e),this.max.max(e),this}expandByVector(e){return this.min.sub(e),this.max.add(e),this}expandByScalar(e){return this.min.addScalar(-e),this.max.addScalar(e),this}expandByObject(e,t=!1){e.updateWorldMatrix(!1,!1);let n=e.geometry;if(n!==void 0){let o=n.getAttribute("position");if(t===!0&&o!==void 0&&e.isInstancedMesh!==!0)for(let l=0,h=o.count;l<h;l++)e.isMesh===!0?e.getVertexPosition(l,qn):qn.fromBufferAttribute(o,l),qn.applyMatrix4(e.matrixWorld),this.expandByPoint(qn);else e.boundingBox!==void 0?(e.boundingBox===null&&e.computeBoundingBox(),ma.copy(e.boundingBox)):(n.boundingBox===null&&n.computeBoundingBox(),ma.copy(n.boundingBox)),ma.applyMatrix4(e.matrixWorld),this.union(ma)}let s=e.children;for(let o=0,l=s.length;o<l;o++)this.expandByObject(s[o],t);return this}containsPoint(e){return e.x>=this.min.x&&e.x<=this.max.x&&e.y>=this.min.y&&e.y<=this.max.y&&e.z>=this.min.z&&e.z<=this.max.z}containsBox(e){return this.min.x<=e.min.x&&e.max.x<=this.max.x&&this.min.y<=e.min.y&&e.max.y<=this.max.y&&this.min.z<=e.min.z&&e.max.z<=this.max.z}getParameter(e,t){return t.set((e.x-this.min.x)/(this.max.x-this.min.x),(e.y-this.min.y)/(this.max.y-this.min.y),(e.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(e){return e.max.x>=this.min.x&&e.min.x<=this.max.x&&e.max.y>=this.min.y&&e.min.y<=this.max.y&&e.max.z>=this.min.z&&e.min.z<=this.max.z}intersectsSphere(e){return this.clampPoint(e.center,qn),qn.distanceToSquared(e.center)<=e.radius*e.radius}intersectsPlane(e){let t,n;return e.normal.x>0?(t=e.normal.x*this.min.x,n=e.normal.x*this.max.x):(t=e.normal.x*this.max.x,n=e.normal.x*this.min.x),e.normal.y>0?(t+=e.normal.y*this.min.y,n+=e.normal.y*this.max.y):(t+=e.normal.y*this.max.y,n+=e.normal.y*this.min.y),e.normal.z>0?(t+=e.normal.z*this.min.z,n+=e.normal.z*this.max.z):(t+=e.normal.z*this.max.z,n+=e.normal.z*this.min.z),t<=-e.constant&&n>=-e.constant}intersectsTriangle(e){if(this.isEmpty())return!1;this.getCenter(rs),ga.subVectors(this.max,rs),Sr.subVectors(e.a,rs),br.subVectors(e.b,rs),Mr.subVectors(e.c,rs),Ci.subVectors(br,Sr),Ri.subVectors(Mr,br),Ji.subVectors(Sr,Mr);let t=[0,-Ci.z,Ci.y,0,-Ri.z,Ri.y,0,-Ji.z,Ji.y,Ci.z,0,-Ci.x,Ri.z,0,-Ri.x,Ji.z,0,-Ji.x,-Ci.y,Ci.x,0,-Ri.y,Ri.x,0,-Ji.y,Ji.x,0];return!$l(t,Sr,br,Mr,ga)||(t=[1,0,0,0,1,0,0,0,1],!$l(t,Sr,br,Mr,ga))?!1:(_a.crossVectors(Ci,Ri),t=[_a.x,_a.y,_a.z],$l(t,Sr,br,Mr,ga))}clampPoint(e,t){return t.copy(e).clamp(this.min,this.max)}distanceToPoint(e){return this.clampPoint(e,qn).distanceTo(e)}getBoundingSphere(e){return this.isEmpty()?e.makeEmpty():(this.getCenter(e.center),e.radius=this.getSize(qn).length()*.5),e}intersect(e){return this.min.max(e.min),this.max.min(e.max),this.isEmpty()&&this.makeEmpty(),this}union(e){return this.min.min(e.min),this.max.max(e.max),this}applyMatrix4(e){return this.isEmpty()?this:(_i[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(e),_i[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(e),_i[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(e),_i[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(e),_i[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(e),_i[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(e),_i[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(e),_i[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(e),this.setFromPoints(_i),this)}translate(e){return this.min.add(e),this.max.add(e),this}equals(e){return e.min.equals(this.min)&&e.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(e){return this.min.fromArray(e.min),this.max.fromArray(e.max),this}},_i=[new j,new j,new j,new j,new j,new j,new j,new j],qn=new j,ma=new oi,Sr=new j,br=new j,Mr=new j,Ci=new j,Ri=new j,Ji=new j,rs=new j,ga=new j,_a=new j,Ki=new j;function $l(i,e,t,n,s){for(let o=0,l=i.length-3;o<=l;o+=3){Ki.fromArray(i,o);let h=s.x*Math.abs(Ki.x)+s.y*Math.abs(Ki.y)+s.z*Math.abs(Ki.z),d=e.dot(Ki),f=t.dot(Ki),g=n.dot(Ki);if(Math.max(-Math.max(d,f,g),Math.min(d,f,g))>h)return!1}return!0}var qt=new j,va=new nt,A0=0,vn=class extends Zn{constructor(e,t,n=!1){if(super(),Array.isArray(e))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:A0++}),this.name="",this.array=e,this.itemSize=t,this.count=e!==void 0?e.length/t:0,this.normalized=n,this.usage=Ku,this.updateRanges=[],this.gpuType=Qn,this.version=0}onUploadCallback(){}set needsUpdate(e){e===!0&&this.version++}setUsage(e){return this.usage=e,this}addUpdateRange(e,t){this.updateRanges.push({start:e,count:t})}clearUpdateRanges(){this.updateRanges.length=0}copy(e){return this.name=e.name,this.array=new e.array.constructor(e.array),this.itemSize=e.itemSize,this.count=e.count,this.normalized=e.normalized,this.usage=e.usage,this.gpuType=e.gpuType,this}copyAt(e,t,n){e*=this.itemSize,n*=t.itemSize;for(let s=0,o=this.itemSize;s<o;s++)this.array[e+s]=t.array[n+s];return this}copyArray(e){return this.array.set(e),this}applyMatrix3(e){if(this.itemSize===2)for(let t=0,n=this.count;t<n;t++)va.fromBufferAttribute(this,t),va.applyMatrix3(e),this.setXY(t,va.x,va.y);else if(this.itemSize===3)for(let t=0,n=this.count;t<n;t++)qt.fromBufferAttribute(this,t),qt.applyMatrix3(e),this.setXYZ(t,qt.x,qt.y,qt.z);return this}applyMatrix4(e){for(let t=0,n=this.count;t<n;t++)qt.fromBufferAttribute(this,t),qt.applyMatrix4(e),this.setXYZ(t,qt.x,qt.y,qt.z);return this}applyNormalMatrix(e){for(let t=0,n=this.count;t<n;t++)qt.fromBufferAttribute(this,t),qt.applyNormalMatrix(e),this.setXYZ(t,qt.x,qt.y,qt.z);return this}transformDirection(e){for(let t=0,n=this.count;t<n;t++)qt.fromBufferAttribute(this,t),qt.transformDirection(e),this.setXYZ(t,qt.x,qt.y,qt.z);return this}set(e,t=0){return this.array.set(e,t),this}getComponent(e,t){let n=this.array[e*this.itemSize+t];return this.normalized&&(n=Cr(n,this.array)),n}setComponent(e,t,n){return this.normalized&&(n=_n(n,this.array)),this.array[e*this.itemSize+t]=n,this}getX(e){let t=this.array[e*this.itemSize];return this.normalized&&(t=Cr(t,this.array)),t}setX(e,t){return this.normalized&&(t=_n(t,this.array)),this.array[e*this.itemSize]=t,this}getY(e){let t=this.array[e*this.itemSize+1];return this.normalized&&(t=Cr(t,this.array)),t}setY(e,t){return this.normalized&&(t=_n(t,this.array)),this.array[e*this.itemSize+1]=t,this}getZ(e){let t=this.array[e*this.itemSize+2];return this.normalized&&(t=Cr(t,this.array)),t}setZ(e,t){return this.normalized&&(t=_n(t,this.array)),this.array[e*this.itemSize+2]=t,this}getW(e){let t=this.array[e*this.itemSize+3];return this.normalized&&(t=Cr(t,this.array)),t}setW(e,t){return this.normalized&&(t=_n(t,this.array)),this.array[e*this.itemSize+3]=t,this}setXY(e,t,n){return e*=this.itemSize,this.normalized&&(t=_n(t,this.array),n=_n(n,this.array)),this.array[e+0]=t,this.array[e+1]=n,this}setXYZ(e,t,n,s){return e*=this.itemSize,this.normalized&&(t=_n(t,this.array),n=_n(n,this.array),s=_n(s,this.array)),this.array[e+0]=t,this.array[e+1]=n,this.array[e+2]=s,this}setXYZW(e,t,n,s,o){return e*=this.itemSize,this.normalized&&(t=_n(t,this.array),n=_n(n,this.array),s=_n(s,this.array),o=_n(o,this.array)),this.array[e+0]=t,this.array[e+1]=n,this.array[e+2]=s,this.array[e+3]=o,this}onUpload(e){return this.onUploadCallback=e,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let e={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return e.name=this.name,e.usage=this.usage,e.gpuType=this.gpuType,e}dispose(){this.dispatchEvent({type:"dispose"})}};var gs=class extends vn{constructor(e,t,n){super(new Uint16Array(e),t,n)}};var _s=class extends vn{constructor(e,t,n){super(new Uint32Array(e),t,n)}};var zt=class extends vn{constructor(e,t,n){super(new Float32Array(e),t,n)}},C0=new oi,ss=new j,jl=new j,ir=class{constructor(e=new j,t=-1){this.isSphere=!0,this.center=e,this.radius=t}set(e,t){return this.center.copy(e),this.radius=t,this}setFromPoints(e,t){let n=this.center;t!==void 0?n.copy(t):C0.setFromPoints(e).getCenter(n);let s=0;for(let o=0,l=e.length;o<l;o++)s=Math.max(s,n.distanceToSquared(e[o]));return this.radius=Math.sqrt(s),this}copy(e){return this.center.copy(e.center),this.radius=e.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(e){return e.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(e){return e.distanceTo(this.center)-this.radius}intersectsSphere(e){let t=this.radius+e.radius;return e.center.distanceToSquared(this.center)<=t*t}intersectsBox(e){return e.intersectsSphere(this)}intersectsPlane(e){return Math.abs(e.distanceToPoint(this.center))<=this.radius}clampPoint(e,t){let n=this.center.distanceToSquared(e);return t.copy(e),n>this.radius*this.radius&&(t.sub(this.center).normalize(),t.multiplyScalar(this.radius).add(this.center)),t}getBoundingBox(e){return this.isEmpty()?(e.makeEmpty(),e):(e.set(this.center,this.center),e.expandByScalar(this.radius),e)}applyMatrix4(e){return this.center.applyMatrix4(e),this.radius=this.radius*e.getMaxScaleOnAxis(),this}translate(e){return this.center.add(e),this}expandByPoint(e){if(this.isEmpty())return this.center.copy(e),this.radius=0,this;ss.subVectors(e,this.center);let t=ss.lengthSq();if(t>this.radius*this.radius){let n=Math.sqrt(t),s=(n-this.radius)*.5;this.center.addScaledVector(ss,s/n),this.radius+=s}return this}union(e){return e.isEmpty()?this:this.isEmpty()?(this.copy(e),this):(this.center.equals(e.center)===!0?this.radius=Math.max(this.radius,e.radius):(jl.subVectors(e.center,this.center).setLength(e.radius),this.expandByPoint(ss.copy(e.center).add(jl)),this.expandByPoint(ss.copy(e.center).sub(jl))),this)}equals(e){return e.center.equals(this.center)&&e.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(e){return this.radius=e.radius,this.center.fromArray(e.center),this}},R0=0,Bn=new Ot,ql=new on,Er=new j,Rn=new oi,as=new oi,sn=new j,Yt=class i extends Zn{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:R0++}),this.uuid=jr(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.indirectOffset=0,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={},this._transformed=!1}getIndex(){return this.index}setIndex(e){return Array.isArray(e)?this.index=new(Q_(e)?_s:gs)(e,1):this.index=e,this}setIndirect(e,t=0){return this.indirect=e,this.indirectOffset=t,this}getIndirect(){return this.indirect}getAttribute(e){return this.attributes[e]}setAttribute(e,t){return this.attributes[e]=t,this}deleteAttribute(e){return delete this.attributes[e],this}hasAttribute(e){return this.attributes[e]!==void 0}addGroup(e,t,n=0){this.groups.push({start:e,count:t,materialIndex:n})}clearGroups(){this.groups=[]}setDrawRange(e,t){this.drawRange.start=e,this.drawRange.count=t}applyMatrix4(e){let t=this.attributes.position;t!==void 0&&(t.applyMatrix4(e),t.needsUpdate=!0);let n=this.attributes.normal;if(n!==void 0){let o=new at().getNormalMatrix(e);n.applyNormalMatrix(o),n.needsUpdate=!0}let s=this.attributes.tangent;return s!==void 0&&(s.transformDirection(e),s.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this._transformed=!0,this}applyQuaternion(e){return Bn.makeRotationFromQuaternion(e),this.applyMatrix4(Bn),this}rotateX(e){return Bn.makeRotationX(e),this.applyMatrix4(Bn),this}rotateY(e){return Bn.makeRotationY(e),this.applyMatrix4(Bn),this}rotateZ(e){return Bn.makeRotationZ(e),this.applyMatrix4(Bn),this}translate(e,t,n){return Bn.makeTranslation(e,t,n),this.applyMatrix4(Bn),this}scale(e,t,n){return Bn.makeScale(e,t,n),this.applyMatrix4(Bn),this}lookAt(e){return ql.lookAt(e),ql.updateMatrix(),this.applyMatrix4(ql.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Er).negate(),this.translate(Er.x,Er.y,Er.z),this}setFromPoints(e){let t=this.getAttribute("position");if(t===void 0){let n=[];for(let s=0,o=e.length;s<o;s++){let l=e[s];n.push(l.x,l.y,l.z||0)}this.setAttribute("position",new zt(n,3))}else{let n=Math.min(e.length,t.count);for(let s=0;s<n;s++){let o=e[s];t.setXYZ(s,o.x,o.y,o.z||0)}e.length>t.count&&et("BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),t.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new oi);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){it("BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new j(-1/0,-1/0,-1/0),new j(1/0,1/0,1/0));return}if(e!==void 0){if(this.boundingBox.setFromBufferAttribute(e),t)for(let n=0,s=t.length;n<s;n++){let o=t[n];Rn.setFromBufferAttribute(o),this.morphTargetsRelative?(sn.addVectors(this.boundingBox.min,Rn.min),this.boundingBox.expandByPoint(sn),sn.addVectors(this.boundingBox.max,Rn.max),this.boundingBox.expandByPoint(sn)):(this.boundingBox.expandByPoint(Rn.min),this.boundingBox.expandByPoint(Rn.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&it('BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new ir);let e=this.attributes.position,t=this.morphAttributes.position;if(e&&e.isGLBufferAttribute){it("BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new j,1/0);return}if(e){let n=this.boundingSphere.center;if(Rn.setFromBufferAttribute(e),t)for(let o=0,l=t.length;o<l;o++){let h=t[o];as.setFromBufferAttribute(h),this.morphTargetsRelative?(sn.addVectors(Rn.min,as.min),Rn.expandByPoint(sn),sn.addVectors(Rn.max,as.max),Rn.expandByPoint(sn)):(Rn.expandByPoint(as.min),Rn.expandByPoint(as.max))}Rn.getCenter(n);let s=0;for(let o=0,l=e.count;o<l;o++)sn.fromBufferAttribute(e,o),s=Math.max(s,n.distanceToSquared(sn));if(t)for(let o=0,l=t.length;o<l;o++){let h=t[o],d=this.morphTargetsRelative;for(let f=0,g=h.count;f<g;f++)sn.fromBufferAttribute(h,f),d&&(Er.fromBufferAttribute(e,f),sn.add(Er)),s=Math.max(s,n.distanceToSquared(sn))}this.boundingSphere.radius=Math.sqrt(s),isNaN(this.boundingSphere.radius)&&it('BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let e=this.index,t=this.attributes;if(e===null||t.position===void 0||t.normal===void 0||t.uv===void 0){it("BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let n=t.position,s=t.normal,o=t.uv,l=this.getAttribute("tangent");(l===void 0||l.count!==n.count)&&(l=new vn(new Float32Array(4*n.count),4),this.setAttribute("tangent",l));let h=[],d=[];for(let w=0;w<n.count;w++)h[w]=new j,d[w]=new j;let f=new j,g=new j,y=new j,m=new nt,S=new nt,T=new nt,P=new j,b=new j;function _(w,D,O){f.fromBufferAttribute(n,w),g.fromBufferAttribute(n,D),y.fromBufferAttribute(n,O),m.fromBufferAttribute(o,w),S.fromBufferAttribute(o,D),T.fromBufferAttribute(o,O),g.sub(f),y.sub(f),S.sub(m),T.sub(m);let q=1/(S.x*T.y-T.x*S.y);isFinite(q)&&(P.copy(g).multiplyScalar(T.y).addScaledVector(y,-S.y).multiplyScalar(q),b.copy(y).multiplyScalar(S.x).addScaledVector(g,-T.x).multiplyScalar(q),h[w].add(P),h[D].add(P),h[O].add(P),d[w].add(b),d[D].add(b),d[O].add(b))}let U=this.groups;U.length===0&&(U=[{start:0,count:e.count}]);for(let w=0,D=U.length;w<D;++w){let O=U[w],q=O.start,Y=O.count;for(let J=q,H=q+Y;J<H;J+=3)_(e.getX(J+0),e.getX(J+1),e.getX(J+2))}let z=new j,R=new j,I=new j,L=new j;function B(w){I.fromBufferAttribute(s,w),L.copy(I);let D=h[w];z.copy(D),z.sub(I.multiplyScalar(I.dot(D))).normalize(),R.crossVectors(L,D);let q=R.dot(d[w])<0?-1:1;l.setXYZW(w,z.x,z.y,z.z,q)}for(let w=0,D=U.length;w<D;++w){let O=U[w],q=O.start,Y=O.count;for(let J=q,H=q+Y;J<H;J+=3)B(e.getX(J+0)),B(e.getX(J+1)),B(e.getX(J+2))}this._transformed=!0}computeVertexNormals(){let e=this.index,t=this.getAttribute("position");if(t!==void 0){let n=this.getAttribute("normal");if(n===void 0||n.count!==t.count)n=new vn(new Float32Array(t.count*3),3),this.setAttribute("normal",n);else for(let m=0,S=n.count;m<S;m++)n.setXYZ(m,0,0,0);let s=new j,o=new j,l=new j,h=new j,d=new j,f=new j,g=new j,y=new j;if(e)for(let m=0,S=e.count;m<S;m+=3){let T=e.getX(m+0),P=e.getX(m+1),b=e.getX(m+2);s.fromBufferAttribute(t,T),o.fromBufferAttribute(t,P),l.fromBufferAttribute(t,b),g.subVectors(l,o),y.subVectors(s,o),g.cross(y),h.fromBufferAttribute(n,T),d.fromBufferAttribute(n,P),f.fromBufferAttribute(n,b),h.add(g),d.add(g),f.add(g),n.setXYZ(T,h.x,h.y,h.z),n.setXYZ(P,d.x,d.y,d.z),n.setXYZ(b,f.x,f.y,f.z)}else for(let m=0,S=t.count;m<S;m+=3)s.fromBufferAttribute(t,m+0),o.fromBufferAttribute(t,m+1),l.fromBufferAttribute(t,m+2),g.subVectors(l,o),y.subVectors(s,o),g.cross(y),n.setXYZ(m+0,g.x,g.y,g.z),n.setXYZ(m+1,g.x,g.y,g.z),n.setXYZ(m+2,g.x,g.y,g.z);this.normalizeNormals(),n.needsUpdate=!0}}normalizeNormals(){let e=this.attributes.normal;for(let t=0,n=e.count;t<n;t++)sn.fromBufferAttribute(e,t),sn.normalize(),e.setXYZ(t,sn.x,sn.y,sn.z)}toNonIndexed(){function e(h,d){let f=h.array,g=h.itemSize,y=h.normalized,m=new f.constructor(d.length*g),S=0,T=0;for(let P=0,b=d.length;P<b;P++){h.isInterleavedBufferAttribute?S=d[P]*h.data.stride+h.offset:S=d[P]*g;for(let _=0;_<g;_++)m[T++]=f[S++]}return new vn(m,g,y)}if(this.index===null)return et("BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let t=new i,n=this.index.array,s=this.attributes;for(let h in s){let d=s[h],f=e(d,n);t.setAttribute(h,f)}let o=this.morphAttributes;for(let h in o){let d=[],f=o[h];for(let g=0,y=f.length;g<y;g++){let m=f[g],S=e(m,n);d.push(S)}t.morphAttributes[h]=d}t.morphTargetsRelative=this.morphTargetsRelative;let l=this.groups;for(let h=0,d=l.length;h<d;h++){let f=l[h];t.addGroup(f.start,f.count,f.materialIndex)}return t}toJSON(){let e={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(e.uuid=this.uuid,e.type=this.parameters!==void 0&&this._transformed===!0?"BufferGeometry":this.type,e.name=this.name,Object.keys(this.userData).length>0&&(e.userData=this.userData),this.parameters!==void 0&&this._transformed!==!0){let d=this.parameters;for(let f in d)d[f]!==void 0&&(e[f]=d[f]);return e}e.data={attributes:{}};let t=this.index;t!==null&&(e.data.index={type:t.array.constructor.name,array:Array.prototype.slice.call(t.array)});let n=this.attributes;for(let d in n){let f=n[d];e.data.attributes[d]=f.toJSON(e.data)}let s={},o=!1;for(let d in this.morphAttributes){let f=this.morphAttributes[d],g=[];for(let y=0,m=f.length;y<m;y++){let S=f[y];g.push(S.toJSON(e.data))}g.length>0&&(s[d]=g,o=!0)}o&&(e.data.morphAttributes=s,e.data.morphTargetsRelative=this.morphTargetsRelative);let l=this.groups;l.length>0&&(e.data.groups=JSON.parse(JSON.stringify(l)));let h=this.boundingSphere;return h!==null&&(e.data.boundingSphere=h.toJSON()),e}clone(){return new this.constructor().copy(this)}copy(e){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let t={};this.name=e.name;let n=e.index;n!==null&&this.setIndex(n.clone());let s=e.attributes;for(let f in s){let g=s[f];this.setAttribute(f,g.clone(t))}let o=e.morphAttributes;for(let f in o){let g=[],y=o[f];for(let m=0,S=y.length;m<S;m++)g.push(y[m].clone(t));this.morphAttributes[f]=g}this.morphTargetsRelative=e.morphTargetsRelative;let l=e.groups;for(let f=0,g=l.length;f<g;f++){let y=l[f];this.addGroup(y.start,y.count,y.materialIndex)}let h=e.boundingBox;h!==null&&(this.boundingBox=h.clone());let d=e.boundingSphere;return d!==null&&(this.boundingSphere=d.clone()),this.drawRange.start=e.drawRange.start,this.drawRange.count=e.drawRange.count,this.userData=e.userData,this._transformed=e._transformed,this}dispose(){this.dispatchEvent({type:"dispose"})}};var Yl=new j,P0=new j,I0=new at,Pn=class{constructor(e=new j(1,0,0),t=0){this.isPlane=!0,this.normal=e,this.constant=t}set(e,t){return this.normal.copy(e),this.constant=t,this}setComponents(e,t,n,s){return this.normal.set(e,t,n),this.constant=s,this}setFromNormalAndCoplanarPoint(e,t){return this.normal.copy(e),this.constant=-t.dot(this.normal),this}setFromCoplanarPoints(e,t,n){let s=Yl.subVectors(n,t).cross(P0.subVectors(e,t)).normalize();return this.setFromNormalAndCoplanarPoint(s,e),this}copy(e){return this.normal.copy(e.normal),this.constant=e.constant,this}normalize(){let e=1/this.normal.length();return this.normal.multiplyScalar(e),this.constant*=e,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(e){return this.normal.dot(e)+this.constant}distanceToSphere(e){return this.distanceToPoint(e.center)-e.radius}projectPoint(e,t){return t.copy(e).addScaledVector(this.normal,-this.distanceToPoint(e))}intersectLine(e,t,n=!0){let s=e.delta(Yl),o=this.normal.dot(s);if(o===0)return this.distanceToPoint(e.start)===0?t.copy(e.start):null;let l=-(e.start.dot(this.normal)+this.constant)/o;return n===!0&&(l<0||l>1)?null:t.copy(e.start).addScaledVector(s,l)}intersectsLine(e){let t=this.distanceToPoint(e.start),n=this.distanceToPoint(e.end);return t<0&&n>0||n<0&&t>0}intersectsBox(e){return e.intersectsPlane(this)}intersectsSphere(e){return e.intersectsPlane(this)}coplanarPoint(e){return e.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(e,t){let n=t||I0.getNormalMatrix(e),s=this.coplanarPoint(Yl).applyMatrix4(e),o=this.normal.applyMatrix3(n).normalize();return this.constant=-s.dot(o),this}translate(e){return this.constant-=e.dot(this.normal),this}equals(e){return e.normal.equals(this.normal)&&e.constant===this.constant}clone(){return new this.constructor().copy(this)}toJSON(){return{normal:this.normal.toArray(),constant:this.constant}}fromJSON(e){return this.normal.fromArray(e.normal),this.constant=e.constant,this}},D0=0,Si=class extends Zn{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:D0++}),this.uuid=jr(),this.name="",this.type="Material",this.blending=Wr,this.side=li,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=pc,this.blendDst=mc,this.blendEquation=ar,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ht(0,0,0),this.blendAlpha=0,this.depthFunc=Pr,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Xu,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Na,this.stencilZFail=Na,this.stencilZPass=Na,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(e){this._alphaTest>0!=e>0&&this.version++,this._alphaTest=e}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(e){if(e!==void 0)for(let t in e){let n=e[t];if(n===void 0){et(`Material: parameter '${t}' has value of undefined.`);continue}let s=this[t];if(s===void 0){et(`Material: '${t}' is not a property of THREE.${this.type}.`);continue}s&&s.isColor?s.set(n):s&&s.isVector2&&n&&n.isVector2||s&&s.isEuler&&n&&n.isEuler||s&&s.isVector3&&n&&n.isVector3?s.copy(n):this[t]=n}}toJSON(e){let t=e===void 0||typeof e=="string";t&&(e={textures:{},images:{}});let n={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};n.uuid=this.uuid,n.type=this.type,n.blending=this.blending,n.side=this.side,n.shadowSide=this.shadowSide,n.vertexColors=this.vertexColors,n.opacity=this.opacity,n.transparent=this.transparent,n.blendSrc=this.blendSrc,n.blendDst=this.blendDst,n.blendEquation=this.blendEquation,n.blendSrcAlpha=this.blendSrcAlpha,n.blendDstAlpha=this.blendDstAlpha,n.blendEquationAlpha=this.blendEquationAlpha,n.blendColor=this.blendColor.getHex(),n.blendAlpha=this.blendAlpha,n.depthFunc=this.depthFunc,n.depthTest=this.depthTest,n.depthWrite=this.depthWrite,n.colorWrite=this.colorWrite,n.clipIntersection=this.clipIntersection,n.clipShadows=this.clipShadows,n.stencilWriteMask=this.stencilWriteMask,n.stencilFunc=this.stencilFunc,n.stencilRef=this.stencilRef,n.stencilFuncMask=this.stencilFuncMask,n.stencilFail=this.stencilFail,n.stencilZFail=this.stencilZFail,n.stencilZPass=this.stencilZPass,n.stencilWrite=this.stencilWrite,n.polygonOffset=this.polygonOffset,n.polygonOffsetFactor=this.polygonOffsetFactor,n.polygonOffsetUnits=this.polygonOffsetUnits,n.dithering=this.dithering,n.alphaTest=this.alphaTest,n.alphaHash=this.alphaHash,n.alphaToCoverage=this.alphaToCoverage,n.premultipliedAlpha=this.premultipliedAlpha,n.forceSinglePass=this.forceSinglePass,n.allowOverride=this.allowOverride,n.visible=this.visible,n.toneMapped=this.toneMapped,n.name=this.name,this.color&&this.color.isColor&&(n.color=this.color.getHex()),this.roughness!==void 0&&(n.roughness=this.roughness),this.metalness!==void 0&&(n.metalness=this.metalness),this.sheen!==void 0&&(n.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(n.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(n.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(n.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&(n.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(n.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(n.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(n.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(n.shininess=this.shininess),this.clearcoat!==void 0&&(n.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(n.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(n.clearcoatMap=this.clearcoatMap.toJSON(e).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(n.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(e).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(n.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(e).uuid,n.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.sheenColorMap&&this.sheenColorMap.isTexture&&(n.sheenColorMap=this.sheenColorMap.toJSON(e).uuid),this.sheenRoughnessMap&&this.sheenRoughnessMap.isTexture&&(n.sheenRoughnessMap=this.sheenRoughnessMap.toJSON(e).uuid),this.dispersion!==void 0&&(n.dispersion=this.dispersion),this.retroreflectivity!==void 0&&(n.retroreflectivity=this.retroreflectivity),this.iridescence!==void 0&&(n.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(n.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(n.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(n.iridescenceMap=this.iridescenceMap.toJSON(e).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(n.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(e).uuid),this.anisotropy!==void 0&&(n.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(n.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(n.anisotropyMap=this.anisotropyMap.toJSON(e).uuid),this.map&&this.map.isTexture&&(n.map=this.map.toJSON(e).uuid),this.matcap&&this.matcap.isTexture&&(n.matcap=this.matcap.toJSON(e).uuid),this.alphaMap&&this.alphaMap.isTexture&&(n.alphaMap=this.alphaMap.toJSON(e).uuid),this.lightMap&&this.lightMap.isTexture&&(n.lightMap=this.lightMap.toJSON(e).uuid,n.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(n.aoMap=this.aoMap.toJSON(e).uuid,n.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(n.bumpMap=this.bumpMap.toJSON(e).uuid,n.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(n.normalMap=this.normalMap.toJSON(e).uuid,n.normalMapType=this.normalMapType,n.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(n.displacementMap=this.displacementMap.toJSON(e).uuid,n.displacementScale=this.displacementScale,n.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(n.roughnessMap=this.roughnessMap.toJSON(e).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(n.metalnessMap=this.metalnessMap.toJSON(e).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(n.emissiveMap=this.emissiveMap.toJSON(e).uuid),this.specularMap&&this.specularMap.isTexture&&(n.specularMap=this.specularMap.toJSON(e).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(n.specularIntensityMap=this.specularIntensityMap.toJSON(e).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(n.specularColorMap=this.specularColorMap.toJSON(e).uuid),this.envMap&&this.envMap.isTexture&&(n.envMap=this.envMap.toJSON(e).uuid,this.combine!==void 0&&(n.combine=this.combine)),this.envMapRotation!==void 0&&(n.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(n.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(n.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(n.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(n.gradientMap=this.gradientMap.toJSON(e).uuid),this.transmission!==void 0&&(n.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(n.transmissionMap=this.transmissionMap.toJSON(e).uuid),this.thickness!==void 0&&(n.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(n.thicknessMap=this.thicknessMap.toJSON(e).uuid),this.attenuationDistance!==void 0&&(n.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(n.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(n.size=this.size),this.sizeAttenuation!==void 0&&(n.sizeAttenuation=this.sizeAttenuation),Array.isArray(this.clippingPlanes)&&this.clippingPlanes.length>0&&(n.clippingPlanes=this.clippingPlanes.map(o=>o.toJSON())),this.rotation!==void 0&&(n.rotation=this.rotation),this.depthPacking!==void 0&&(n.depthPacking=this.depthPacking),this.linewidth!==void 0&&(n.linewidth=this.linewidth),this.linecap!==void 0&&(n.linecap=this.linecap),this.linejoin!==void 0&&(n.linejoin=this.linejoin),this.dashSize!==void 0&&(n.dashSize=this.dashSize),this.gapSize!==void 0&&(n.gapSize=this.gapSize),this.scale!==void 0&&(n.scale=this.scale),this.wireframe!==void 0&&(n.wireframe=this.wireframe),this.wireframeLinewidth!==void 0&&(n.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!==void 0&&(n.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!==void 0&&(n.wireframeLinejoin=this.wireframeLinejoin),this.flatShading!==void 0&&(n.flatShading=this.flatShading),this.fog!==void 0&&(n.fog=this.fog),Object.keys(this.userData).length>0&&(n.userData=this.userData);function s(o){let l=[];for(let h in o){let d=o[h];delete d.metadata,l.push(d)}return l}if(t){let o=s(e.textures),l=s(e.images);o.length>0&&(n.textures=o),l.length>0&&(n.images=l)}return n}fromJSON(e,t){if(e.uuid!==void 0&&(this.uuid=e.uuid),e.name!==void 0&&(this.name=e.name),e.color!==void 0&&this.color!==void 0&&this.color.setHex(e.color),e.roughness!==void 0&&(this.roughness=e.roughness),e.metalness!==void 0&&(this.metalness=e.metalness),e.sheen!==void 0&&(this.sheen=e.sheen),e.sheenColor!==void 0&&(this.sheenColor=new ht().setHex(e.sheenColor)),e.sheenRoughness!==void 0&&(this.sheenRoughness=e.sheenRoughness),e.emissive!==void 0&&this.emissive!==void 0&&this.emissive.setHex(e.emissive),e.specular!==void 0&&this.specular!==void 0&&this.specular.setHex(e.specular),e.specularIntensity!==void 0&&(this.specularIntensity=e.specularIntensity),e.specularColor!==void 0&&this.specularColor!==void 0&&this.specularColor.setHex(e.specularColor),e.shininess!==void 0&&(this.shininess=e.shininess),e.clearcoat!==void 0&&(this.clearcoat=e.clearcoat),e.clearcoatRoughness!==void 0&&(this.clearcoatRoughness=e.clearcoatRoughness),e.dispersion!==void 0&&(this.dispersion=e.dispersion),e.retroreflectivity!==void 0&&(this.retroreflectivity=e.retroreflectivity),e.iridescence!==void 0&&(this.iridescence=e.iridescence),e.iridescenceIOR!==void 0&&(this.iridescenceIOR=e.iridescenceIOR),e.iridescenceThicknessRange!==void 0&&(this.iridescenceThicknessRange=e.iridescenceThicknessRange),e.transmission!==void 0&&(this.transmission=e.transmission),e.thickness!==void 0&&(this.thickness=e.thickness),e.attenuationDistance!==void 0&&(this.attenuationDistance=e.attenuationDistance),e.attenuationColor!==void 0&&this.attenuationColor!==void 0&&this.attenuationColor.setHex(e.attenuationColor),e.anisotropy!==void 0&&(this.anisotropy=e.anisotropy),e.anisotropyRotation!==void 0&&(this.anisotropyRotation=e.anisotropyRotation),e.fog!==void 0&&(this.fog=e.fog),e.flatShading!==void 0&&(this.flatShading=e.flatShading),e.blending!==void 0&&(this.blending=e.blending),e.combine!==void 0&&(this.combine=e.combine),e.side!==void 0&&(this.side=e.side),e.shadowSide!==void 0&&(this.shadowSide=e.shadowSide),e.opacity!==void 0&&(this.opacity=e.opacity),e.transparent!==void 0&&(this.transparent=e.transparent),e.alphaTest!==void 0&&(this.alphaTest=e.alphaTest),e.alphaHash!==void 0&&(this.alphaHash=e.alphaHash),e.depthFunc!==void 0&&(this.depthFunc=e.depthFunc),e.depthTest!==void 0&&(this.depthTest=e.depthTest),e.depthWrite!==void 0&&(this.depthWrite=e.depthWrite),e.colorWrite!==void 0&&(this.colorWrite=e.colorWrite),e.clippingPlanes!==void 0&&(this.clippingPlanes=e.clippingPlanes.map(n=>new Pn().fromJSON(n))),e.clipIntersection!==void 0&&(this.clipIntersection=e.clipIntersection),e.clipShadows!==void 0&&(this.clipShadows=e.clipShadows),e.depthPacking!==void 0&&(this.depthPacking=e.depthPacking),e.blendSrc!==void 0&&(this.blendSrc=e.blendSrc),e.blendDst!==void 0&&(this.blendDst=e.blendDst),e.blendEquation!==void 0&&(this.blendEquation=e.blendEquation),e.blendSrcAlpha!==void 0&&(this.blendSrcAlpha=e.blendSrcAlpha),e.blendDstAlpha!==void 0&&(this.blendDstAlpha=e.blendDstAlpha),e.blendEquationAlpha!==void 0&&(this.blendEquationAlpha=e.blendEquationAlpha),e.blendColor!==void 0&&this.blendColor!==void 0&&this.blendColor.setHex(e.blendColor),e.blendAlpha!==void 0&&(this.blendAlpha=e.blendAlpha),e.stencilWriteMask!==void 0&&(this.stencilWriteMask=e.stencilWriteMask),e.stencilFunc!==void 0&&(this.stencilFunc=e.stencilFunc),e.stencilRef!==void 0&&(this.stencilRef=e.stencilRef),e.stencilFuncMask!==void 0&&(this.stencilFuncMask=e.stencilFuncMask),e.stencilFail!==void 0&&(this.stencilFail=e.stencilFail),e.stencilZFail!==void 0&&(this.stencilZFail=e.stencilZFail),e.stencilZPass!==void 0&&(this.stencilZPass=e.stencilZPass),e.stencilWrite!==void 0&&(this.stencilWrite=e.stencilWrite),e.wireframe!==void 0&&(this.wireframe=e.wireframe),e.wireframeLinewidth!==void 0&&(this.wireframeLinewidth=e.wireframeLinewidth),e.wireframeLinecap!==void 0&&(this.wireframeLinecap=e.wireframeLinecap),e.wireframeLinejoin!==void 0&&(this.wireframeLinejoin=e.wireframeLinejoin),e.rotation!==void 0&&(this.rotation=e.rotation),e.linewidth!==void 0&&(this.linewidth=e.linewidth),e.linecap!==void 0&&(this.linecap=e.linecap),e.linejoin!==void 0&&(this.linejoin=e.linejoin),e.dashSize!==void 0&&(this.dashSize=e.dashSize),e.gapSize!==void 0&&(this.gapSize=e.gapSize),e.scale!==void 0&&(this.scale=e.scale),e.polygonOffset!==void 0&&(this.polygonOffset=e.polygonOffset),e.polygonOffsetFactor!==void 0&&(this.polygonOffsetFactor=e.polygonOffsetFactor),e.polygonOffsetUnits!==void 0&&(this.polygonOffsetUnits=e.polygonOffsetUnits),e.dithering!==void 0&&(this.dithering=e.dithering),e.alphaToCoverage!==void 0&&(this.alphaToCoverage=e.alphaToCoverage),e.premultipliedAlpha!==void 0&&(this.premultipliedAlpha=e.premultipliedAlpha),e.forceSinglePass!==void 0&&(this.forceSinglePass=e.forceSinglePass),e.allowOverride!==void 0&&(this.allowOverride=e.allowOverride),e.visible!==void 0&&(this.visible=e.visible),e.toneMapped!==void 0&&(this.toneMapped=e.toneMapped),e.userData!==void 0&&(this.userData=e.userData),e.vertexColors!==void 0&&(typeof e.vertexColors=="number"?this.vertexColors=e.vertexColors>0:this.vertexColors=e.vertexColors),e.size!==void 0&&(this.size=e.size),e.sizeAttenuation!==void 0&&(this.sizeAttenuation=e.sizeAttenuation),e.map!==void 0&&(this.map=t[e.map]||null),e.matcap!==void 0&&(this.matcap=t[e.matcap]||null),e.alphaMap!==void 0&&(this.alphaMap=t[e.alphaMap]||null),e.bumpMap!==void 0&&(this.bumpMap=t[e.bumpMap]||null),e.bumpScale!==void 0&&(this.bumpScale=e.bumpScale),e.normalMap!==void 0&&(this.normalMap=t[e.normalMap]||null),e.normalMapType!==void 0&&(this.normalMapType=e.normalMapType),e.normalScale!==void 0){let n=e.normalScale;Array.isArray(n)===!1&&(n=[n,n]),this.normalScale=new nt().fromArray(n)}return e.displacementMap!==void 0&&(this.displacementMap=t[e.displacementMap]||null),e.displacementScale!==void 0&&(this.displacementScale=e.displacementScale),e.displacementBias!==void 0&&(this.displacementBias=e.displacementBias),e.roughnessMap!==void 0&&(this.roughnessMap=t[e.roughnessMap]||null),e.metalnessMap!==void 0&&(this.metalnessMap=t[e.metalnessMap]||null),e.emissiveMap!==void 0&&(this.emissiveMap=t[e.emissiveMap]||null),e.emissiveIntensity!==void 0&&(this.emissiveIntensity=e.emissiveIntensity),e.specularMap!==void 0&&(this.specularMap=t[e.specularMap]||null),e.specularIntensityMap!==void 0&&(this.specularIntensityMap=t[e.specularIntensityMap]||null),e.specularColorMap!==void 0&&(this.specularColorMap=t[e.specularColorMap]||null),e.envMap!==void 0&&(this.envMap=t[e.envMap]||null),e.envMapRotation!==void 0&&this.envMapRotation.fromArray(e.envMapRotation),e.envMapIntensity!==void 0&&(this.envMapIntensity=e.envMapIntensity),e.reflectivity!==void 0&&(this.reflectivity=e.reflectivity),e.refractionRatio!==void 0&&(this.refractionRatio=e.refractionRatio),e.lightMap!==void 0&&(this.lightMap=t[e.lightMap]||null),e.lightMapIntensity!==void 0&&(this.lightMapIntensity=e.lightMapIntensity),e.aoMap!==void 0&&(this.aoMap=t[e.aoMap]||null),e.aoMapIntensity!==void 0&&(this.aoMapIntensity=e.aoMapIntensity),e.gradientMap!==void 0&&(this.gradientMap=t[e.gradientMap]||null),e.clearcoatMap!==void 0&&(this.clearcoatMap=t[e.clearcoatMap]||null),e.clearcoatRoughnessMap!==void 0&&(this.clearcoatRoughnessMap=t[e.clearcoatRoughnessMap]||null),e.clearcoatNormalMap!==void 0&&(this.clearcoatNormalMap=t[e.clearcoatNormalMap]||null),e.clearcoatNormalScale!==void 0&&(this.clearcoatNormalScale=new nt().fromArray(e.clearcoatNormalScale)),e.iridescenceMap!==void 0&&(this.iridescenceMap=t[e.iridescenceMap]||null),e.iridescenceThicknessMap!==void 0&&(this.iridescenceThicknessMap=t[e.iridescenceThicknessMap]||null),e.transmissionMap!==void 0&&(this.transmissionMap=t[e.transmissionMap]||null),e.thicknessMap!==void 0&&(this.thicknessMap=t[e.thicknessMap]||null),e.anisotropyMap!==void 0&&(this.anisotropyMap=t[e.anisotropyMap]||null),e.sheenColorMap!==void 0&&(this.sheenColorMap=t[e.sheenColorMap]||null),e.sheenRoughnessMap!==void 0&&(this.sheenRoughnessMap=t[e.sheenRoughnessMap]||null),this}clone(){return new this.constructor().copy(this)}copy(e){this.name=e.name,this.blending=e.blending,this.side=e.side,this.vertexColors=e.vertexColors,this.opacity=e.opacity,this.transparent=e.transparent,this.blendSrc=e.blendSrc,this.blendDst=e.blendDst,this.blendEquation=e.blendEquation,this.blendSrcAlpha=e.blendSrcAlpha,this.blendDstAlpha=e.blendDstAlpha,this.blendEquationAlpha=e.blendEquationAlpha,this.blendColor.copy(e.blendColor),this.blendAlpha=e.blendAlpha,this.depthFunc=e.depthFunc,this.depthTest=e.depthTest,this.depthWrite=e.depthWrite,this.stencilWriteMask=e.stencilWriteMask,this.stencilFunc=e.stencilFunc,this.stencilRef=e.stencilRef,this.stencilFuncMask=e.stencilFuncMask,this.stencilFail=e.stencilFail,this.stencilZFail=e.stencilZFail,this.stencilZPass=e.stencilZPass,this.stencilWrite=e.stencilWrite;let t=e.clippingPlanes,n=null;if(t!==null){let s=t.length;n=new Array(s);for(let o=0;o!==s;++o)n[o]=t[o].clone()}return this.clippingPlanes=n,this.clipIntersection=e.clipIntersection,this.clipShadows=e.clipShadows,this.shadowSide=e.shadowSide,this.colorWrite=e.colorWrite,this.precision=e.precision,this.polygonOffset=e.polygonOffset,this.polygonOffsetFactor=e.polygonOffsetFactor,this.polygonOffsetUnits=e.polygonOffsetUnits,this.dithering=e.dithering,this.alphaTest=e.alphaTest,this.alphaHash=e.alphaHash,this.alphaToCoverage=e.alphaToCoverage,this.premultipliedAlpha=e.premultipliedAlpha,this.forceSinglePass=e.forceSinglePass,this.allowOverride=e.allowOverride,this.visible=e.visible,this.toneMapped=e.toneMapped,this.userData=JSON.parse(JSON.stringify(e.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(e){e===!0&&this.version++}};var vi=new j,Zl=new j,ya=new j,xa=new j,Di=class{constructor(e=new j,t=new j(0,0,-1)){this.origin=e,this.direction=t}set(e,t){return this.origin.copy(e),this.direction.copy(t),this}copy(e){return this.origin.copy(e.origin),this.direction.copy(e.direction),this}at(e,t){return t.copy(this.origin).addScaledVector(this.direction,e)}lookAt(e){return this.direction.copy(e).sub(this.origin).normalize(),this}recast(e){return this.origin.copy(this.at(e,vi)),this}closestPointToPoint(e,t){t.subVectors(e,this.origin);let n=t.dot(this.direction);return n<0?t.copy(this.origin):t.copy(this.origin).addScaledVector(this.direction,n)}distanceToPoint(e){return Math.sqrt(this.distanceSqToPoint(e))}distanceSqToPoint(e){let t=vi.subVectors(e,this.origin).dot(this.direction);return t<0?this.origin.distanceToSquared(e):(vi.copy(this.origin).addScaledVector(this.direction,t),vi.distanceToSquared(e))}distanceSqToSegment(e,t,n,s){Zl.copy(e).add(t).multiplyScalar(.5),ya.copy(t).sub(e).normalize(),xa.copy(this.origin).sub(Zl);let o=e.distanceTo(t)*.5,l=-this.direction.dot(ya),h=xa.dot(this.direction),d=-xa.dot(ya),f=xa.lengthSq(),g=Math.abs(1-l*l),y,m,S,T;if(g>0)if(y=l*d-h,m=l*h-d,T=o*g,y>=0)if(m>=-T)if(m<=T){let P=1/g;y*=P,m*=P,S=y*(y+l*m+2*h)+m*(l*y+m+2*d)+f}else m=o,y=Math.max(0,-(l*m+h)),S=-y*y+m*(m+2*d)+f;else m=-o,y=Math.max(0,-(l*m+h)),S=-y*y+m*(m+2*d)+f;else m<=-T?(y=Math.max(0,-(-l*o+h)),m=y>0?-o:Math.min(Math.max(-o,-d),o),S=-y*y+m*(m+2*d)+f):m<=T?(y=0,m=Math.min(Math.max(-o,-d),o),S=m*(m+2*d)+f):(y=Math.max(0,-(l*o+h)),m=y>0?o:Math.min(Math.max(-o,-d),o),S=-y*y+m*(m+2*d)+f);else m=l>0?-o:o,y=Math.max(0,-(l*m+h)),S=-y*y+m*(m+2*d)+f;return n&&n.copy(this.origin).addScaledVector(this.direction,y),s&&s.copy(Zl).addScaledVector(ya,m),S}intersectSphere(e,t){if(e.radius<0)return null;vi.subVectors(e.center,this.origin);let n=vi.dot(this.direction),s=vi.dot(vi)-n*n,o=e.radius*e.radius;if(s>o)return null;let l=Math.sqrt(o-s),h=n-l,d=n+l;return d<0?null:h<0?this.at(d,t):this.at(h,t)}intersectsSphere(e){return e.radius<0?!1:this.distanceSqToPoint(e.center)<=e.radius*e.radius}distanceToPlane(e){let t=e.normal.dot(this.direction);if(t===0)return e.distanceToPoint(this.origin)===0?0:null;let n=-(this.origin.dot(e.normal)+e.constant)/t;return n>=0?n:null}intersectPlane(e,t){let n=this.distanceToPlane(e);return n===null?null:this.at(n,t)}intersectsPlane(e){let t=e.distanceToPoint(this.origin);return t===0||e.normal.dot(this.direction)*t<0}intersectBox(e,t){let n,s,o,l,h,d,f=1/this.direction.x,g=1/this.direction.y,y=1/this.direction.z,m=this.origin;return f>=0?(n=(e.min.x-m.x)*f,s=(e.max.x-m.x)*f):(n=(e.max.x-m.x)*f,s=(e.min.x-m.x)*f),g>=0?(o=(e.min.y-m.y)*g,l=(e.max.y-m.y)*g):(o=(e.max.y-m.y)*g,l=(e.min.y-m.y)*g),n>l||o>s||((o>n||isNaN(n))&&(n=o),(l<s||isNaN(s))&&(s=l),y>=0?(h=(e.min.z-m.z)*y,d=(e.max.z-m.z)*y):(h=(e.max.z-m.z)*y,d=(e.min.z-m.z)*y),n>d||h>s)||((h>n||n!==n)&&(n=h),(d<s||s!==s)&&(s=d),s<0)?null:this.at(n>=0?n:s,t)}intersectsBox(e){return this.intersectBox(e,vi)!==null}intersectTriangle(e,t,n,s,o){let l=this.origin,h=this.direction,d=h.x,f=h.y,g=h.z,y=e.x-l.x,m=e.y-l.y,S=e.z-l.z,T=t.x-l.x,P=t.y-l.y,b=t.z-l.z,_=n.x-l.x,U=n.y-l.y,z=n.z-l.z,R=Math.abs(d),I=Math.abs(f),L=Math.abs(g),B,w,D,O,q,Y,J,H,te,k,se,_e;if(R>=I&&R>=L?(D=d,Y=y,te=T,_e=_,d>=0?(B=f,w=g,O=m,q=S,J=P,H=b,k=U,se=z):(B=g,w=f,O=S,q=m,J=b,H=P,k=z,se=U)):I>=L?(D=f,Y=m,te=P,_e=U,f>=0?(B=g,w=d,O=S,q=y,J=b,H=T,k=z,se=_):(B=d,w=g,O=y,q=S,J=T,H=b,k=_,se=z)):(D=g,Y=S,te=b,_e=z,g>=0?(B=d,w=f,O=y,q=m,J=T,H=P,k=_,se=U):(B=f,w=d,O=m,q=y,J=P,H=T,k=U,se=_)),D===0)return null;let ae=B/D,V=w/D,ge=1/D,Ye=O-ae*Y,$e=q-V*Y,Ut=J-ae*te,mt=H-V*te,Ke=k-ae*_e,le=se-V*_e,fe=Ke*mt-le*Ut,ke=Ye*le-$e*Ke,st=Ut*$e-mt*Ye;if(s){if(fe<0||ke<0||st<0)return null}else if((fe<0||ke<0||st<0)&&(fe>0||ke>0||st>0))return null;let Be=fe+ke+st;if(Be===0)return null;let ut=ge*(fe*Y+ke*te+st*_e);return(Be>0?ut<0:ut>0)?null:this.at(ut/Be,o)}applyMatrix4(e){return this.origin.applyMatrix4(e),this.direction.transformDirection(e),this}equals(e){return e.origin.equals(this.origin)&&e.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},Or=class extends Si{constructor(e){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ht(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xi,this.combine=vo,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.fog=e.fog,this}},iu=new Ot,Qi=new Di,Sa=new ir,ru=new j,ba=new j,Ma=new j,Ea=new j,Jl=new j,wa=new j,su=new j,Ta=new j,yn=class extends on{constructor(e=new Yt,t=new Or){super(),this.isMesh=!0,this.type="Mesh",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),e.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=e.morphTargetInfluences.slice()),e.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},e.morphTargetDictionary)),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}updateMorphTargets(){let t=this.geometry.morphAttributes,n=Object.keys(t);if(n.length>0){let s=t[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let o=0,l=s.length;o<l;o++){let h=s[o].name||String(o);this.morphTargetInfluences.push(0),this.morphTargetDictionary[h]=o}}}}getVertexPosition(e,t){let n=this.geometry,s=n.attributes.position,o=n.morphAttributes.position,l=n.morphTargetsRelative;t.fromBufferAttribute(s,e);let h=this.morphTargetInfluences;if(o&&h){wa.set(0,0,0);for(let d=0,f=o.length;d<f;d++){let g=h[d],y=o[d];g!==0&&(Jl.fromBufferAttribute(y,e),l?wa.addScaledVector(Jl,g):wa.addScaledVector(Jl.sub(t),g))}t.add(wa)}return t}intersectsFrustum(e){return e.intersectsObject(this)}raycast(e,t){let n=this.geometry,s=this.material,o=this.matrixWorld;s!==void 0&&(n.boundingSphere===null&&n.computeBoundingSphere(),Sa.copy(n.boundingSphere),Sa.applyMatrix4(o),Qi.copy(e.ray).recast(e.near),!(Sa.containsPoint(Qi.origin)===!1&&(Qi.intersectSphere(Sa,ru)===null||Qi.origin.distanceToSquared(ru)>(e.far-e.near)**2))&&(iu.copy(o).invert(),Qi.copy(e.ray).applyMatrix4(iu),!(n.boundingBox!==null&&Qi.intersectsBox(n.boundingBox)===!1)&&this._computeIntersections(e,t,Qi)))}_computeIntersections(e,t,n){let s,o=this.geometry,l=this.material,h=o.index,d=o.attributes.position,f=o.attributes.uv,g=o.attributes.uv1,y=o.attributes.normal,m=o.groups,S=o.drawRange;if(h!==null)if(Array.isArray(l))for(let T=0,P=m.length;T<P;T++){let b=m[T],_=l[b.materialIndex],U=Math.max(b.start,S.start),z=Math.min(h.count,Math.min(b.start+b.count,S.start+S.count));for(let R=U,I=z;R<I;R+=3){let L=h.getX(R),B=h.getX(R+1),w=h.getX(R+2);s=Aa(this,_,e,n,f,g,y,L,B,w),s&&(s.faceIndex=Math.floor(R/3),s.face.materialIndex=b.materialIndex,t.push(s))}}else{let T=Math.max(0,S.start),P=Math.min(h.count,S.start+S.count);for(let b=T,_=P;b<_;b+=3){let U=h.getX(b),z=h.getX(b+1),R=h.getX(b+2);s=Aa(this,l,e,n,f,g,y,U,z,R),s&&(s.faceIndex=Math.floor(b/3),t.push(s))}}else if(d!==void 0)if(Array.isArray(l))for(let T=0,P=m.length;T<P;T++){let b=m[T],_=l[b.materialIndex],U=Math.max(b.start,S.start),z=Math.min(d.count,Math.min(b.start+b.count,S.start+S.count));for(let R=U,I=z;R<I;R+=3){let L=R,B=R+1,w=R+2;s=Aa(this,_,e,n,f,g,y,L,B,w),s&&(s.faceIndex=Math.floor(R/3),s.face.materialIndex=b.materialIndex,t.push(s))}}else{let T=Math.max(0,S.start),P=Math.min(d.count,S.start+S.count);for(let b=T,_=P;b<_;b+=3){let U=b,z=b+1,R=b+2;s=Aa(this,l,e,n,f,g,y,U,z,R),s&&(s.faceIndex=Math.floor(b/3),t.push(s))}}}};function L0(i,e,t,n,s,o,l,h){let d;if(e.side===xn?d=n.intersectTriangle(l,o,s,!0,h):d=n.intersectTriangle(s,o,l,e.side===li,h),d===null)return null;Ta.copy(h),Ta.applyMatrix4(i.matrixWorld);let f=t.ray.origin.distanceTo(Ta);return f<t.near||f>t.far?null:{distance:f,point:Ta.clone(),object:i}}function Aa(i,e,t,n,s,o,l,h,d,f){i.getVertexPosition(h,ba),i.getVertexPosition(d,Ma),i.getVertexPosition(f,Ea);let g=L0(i,e,t,n,ba,Ma,Ea,su);if(g){let y=new j;Ii.getBarycoord(su,ba,Ma,Ea,y),s&&(g.uv=Ii.getInterpolatedAttribute(s,h,d,f,y,new nt)),o&&(g.uv1=Ii.getInterpolatedAttribute(o,h,d,f,y,new nt)),l&&(g.normal=Ii.getInterpolatedAttribute(l,h,d,f,y,new j),g.normal.dot(n.direction)>0&&g.normal.multiplyScalar(-1));let m={a:h,b:d,c:f,normal:new j,materialIndex:0};Ii.getNormal(ba,Ma,Ea,m.normal),g.face=m,g.barycoord=y}return g}var Ya=class extends bn{constructor(e=null,t=1,n=1,s,o,l,h,d,f=an,g=an,y,m){super(null,l,h,d,f,g,s,o,y,m),this.isDataTexture=!0,this.image={data:e,width:t,height:n},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var er=new ir,F0=new nt(.5,.5),Ca=new j,Br=class{constructor(e=new Pn,t=new Pn,n=new Pn,s=new Pn,o=new Pn,l=new Pn){this.planes=[e,t,n,s,o,l]}set(e,t,n,s,o,l){let h=this.planes;return h[0].copy(e),h[1].copy(t),h[2].copy(n),h[3].copy(s),h[4].copy(o),h[5].copy(l),this}copy(e){let t=this.planes;for(let n=0;n<6;n++)t[n].copy(e.planes[n]);return this}setFromProjectionMatrix(e,t=Yn,n=!1){let s=this.planes,o=e.elements,l=o[0],h=o[1],d=o[2],f=o[3],g=o[4],y=o[5],m=o[6],S=o[7],T=o[8],P=o[9],b=o[10],_=o[11],U=o[12],z=o[13],R=o[14],I=o[15];if(s[0].setComponents(f-l,S-g,_-T,I-U).normalize(),s[1].setComponents(f+l,S+g,_+T,I+U).normalize(),s[2].setComponents(f+h,S+y,_+P,I+z).normalize(),s[3].setComponents(f-h,S-y,_-P,I-z).normalize(),n)s[4].setComponents(d,m,b,R).normalize(),s[5].setComponents(f-d,S-m,_-b,I-R).normalize();else if(s[4].setComponents(f-d,S-m,_-b,I-R).normalize(),t===Yn)s[5].setComponents(f+d,S+m,_+b,I+R).normalize();else if(t===Ir)s[5].setComponents(d,m,b,R).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+t);return this}intersectsObject(e){if(e.boundingSphere!==void 0)e.boundingSphere===null&&e.computeBoundingSphere(),er.copy(e.boundingSphere).applyMatrix4(e.matrixWorld);else{let t=e.geometry;t.boundingSphere===null&&t.computeBoundingSphere(),er.copy(t.boundingSphere).applyMatrix4(e.matrixWorld)}return this.intersectsSphere(er)}intersectsSprite(e){er.center.set(0,0,0);let t=F0.distanceTo(e.center);return er.radius=.7071067811865476+t,er.applyMatrix4(e.matrixWorld),this.intersectsSphere(er)}intersectsSphere(e){let t=this.planes,n=e.center,s=-e.radius;for(let o=0;o<6;o++)if(t[o].distanceToPoint(n)<s)return!1;return!0}intersectsBox(e){let t=this.planes;for(let n=0;n<6;n++){let s=t[n];if(Ca.x=s.normal.x>0?e.max.x:e.min.x,Ca.y=s.normal.y>0?e.max.y:e.min.y,Ca.z=s.normal.z>0?e.max.z:e.min.z,s.distanceToPoint(Ca)<0)return!1}return!0}containsPoint(e){let t=this.planes;for(let n=0;n<6;n++)if(t[n].distanceToPoint(e)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}};var kr=class extends Si{constructor(e){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ht(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.map=e.map,this.linewidth=e.linewidth,this.linecap=e.linecap,this.linejoin=e.linejoin,this.fog=e.fog,this}},Za=new j,Ja=new j,au=new Ot,os=new Di,Ra=new ir,Kl=new j,ou=new j,vs=class extends on{constructor(e=new Yt,t=new kr){super(),this.isLine=!0,this.type="Line",this.geometry=e,this.material=t,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(e,t){return super.copy(e,t),this.material=Array.isArray(e.material)?e.material.slice():e.material,this.geometry=e.geometry,this}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,n=[0];for(let s=1,o=t.count;s<o;s++)Za.fromBufferAttribute(t,s-1),Ja.fromBufferAttribute(t,s),n[s]=n[s-1],n[s]+=Za.distanceTo(Ja);e.setAttribute("lineDistance",new zt(n,1))}else et("Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}intersectsFrustum(e){return e.intersectsObject(this)}raycast(e,t){let n=this.geometry,s=this.matrixWorld,o=e.params.Line.threshold,l=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),Ra.copy(n.boundingSphere),Ra.applyMatrix4(s),Ra.radius+=o,e.ray.intersectsSphere(Ra)===!1)return;au.copy(s).invert(),os.copy(e.ray).applyMatrix4(au);let h=o/((this.scale.x+this.scale.y+this.scale.z)/3),d=h*h,f=this.isLineSegments?2:1,g=n.index,m=n.attributes.position;if(g!==null){let S=Math.max(0,l.start),T=Math.min(g.count,l.start+l.count);for(let P=S,b=T-1;P<b;P+=f){let _=g.getX(P),U=g.getX(P+1),z=Pa(this,e,os,d,_,U,P);z&&t.push(z)}if(this.isLineLoop){let P=g.getX(T-1),b=g.getX(S),_=Pa(this,e,os,d,P,b,T-1);_&&t.push(_)}}else{let S=Math.max(0,l.start),T=Math.min(m.count,l.start+l.count);for(let P=S,b=T-1;P<b;P+=f){let _=Pa(this,e,os,d,P,P+1,P);_&&t.push(_)}if(this.isLineLoop){let P=Pa(this,e,os,d,T-1,S,T-1);P&&t.push(P)}}}updateMorphTargets(){let t=this.geometry.morphAttributes,n=Object.keys(t);if(n.length>0){let s=t[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let o=0,l=s.length;o<l;o++){let h=s[o].name||String(o);this.morphTargetInfluences.push(0),this.morphTargetDictionary[h]=o}}}}};function Pa(i,e,t,n,s,o,l){let h=i.geometry.attributes.position;if(Za.fromBufferAttribute(h,s),Ja.fromBufferAttribute(h,o),t.distanceSqToSegment(Za,Ja,Kl,ou)>n)return;Kl.applyMatrix4(i.matrixWorld);let f=e.ray.origin.distanceTo(Kl);if(!(f<e.near||f>e.far))return{distance:f,point:ou.clone().applyMatrix4(i.matrixWorld),index:l,face:null,faceIndex:null,barycoord:null,object:i}}var lu=new j,cu=new j,Ka=class extends vs{constructor(e,t){super(e,t),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){let e=this.geometry;if(e.index===null){let t=e.attributes.position,n=[];for(let s=0,o=t.count;s<o;s+=2)lu.fromBufferAttribute(t,s),cu.fromBufferAttribute(t,s+1),n[s]=s===0?0:n[s-1],n[s+1]=n[s]+lu.distanceTo(cu);e.setAttribute("lineDistance",new zt(n,1))}else et("LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}};var ys=class extends bn{constructor(e=[],t=zi,n,s,o,l,h,d,f,g){super(e,t,n,s,o,l,h,d,f,g),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(e){this.image=e}};var Li=class extends bn{constructor(e,t,n=Kn,s,o,l,h=an,d=an,f,g=ai,y=1){if(g!==ai&&g!==Gi)throw new Error("THREE.DepthTexture: format must be either THREE.DepthFormat or THREE.DepthStencilFormat");let m={width:e,height:t,depth:y};super(m,s,o,l,h,d,g,n,f),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(e){return super.copy(e),this.source=new Fr(Object.assign({},e.image)),this.compareFunction=e.compareFunction,this}toJSON(e){let t=super.toJSON(e);return t.compareFunction=this.compareFunction,t}},Qa=class extends Li{constructor(e,t=Kn,n=zi,s,o,l=an,h=an,d,f=ai){let g={width:e,height:e,depth:1},y=[g,g,g,g,g,g];super(e,e,t,n,s,o,l,h,d,f),this.image=y,this.isCubeDepthTexture=!0,this.isCubeTexture=!0}get images(){return this.image}set images(e){this.image=e}},xs=class extends bn{constructor(e=null){super(),this.sourceTexture=e,this.isExternalTexture=!0}copy(e){return super.copy(e),this.sourceTexture=e.sourceTexture,this}},Fi=class i extends Yt{constructor(e=1,t=1,n=1,s=1,o=1,l=1){super(),this.type="BoxGeometry",this.parameters={width:e,height:t,depth:n,widthSegments:s,heightSegments:o,depthSegments:l};let h=this;s=Math.floor(s),o=Math.floor(o),l=Math.floor(l);let d=[],f=[],g=[],y=[],m=0,S=0;T("z","y","x",-1,-1,n,t,e,l,o,0),T("z","y","x",1,-1,n,t,-e,l,o,1),T("x","z","y",1,1,e,n,t,s,l,2),T("x","z","y",1,-1,e,n,-t,s,l,3),T("x","y","z",1,-1,e,t,n,s,o,4),T("x","y","z",-1,-1,e,t,-n,s,o,5),this.setIndex(d),this.setAttribute("position",new zt(f,3)),this.setAttribute("normal",new zt(g,3)),this.setAttribute("uv",new zt(y,2));function T(P,b,_,U,z,R,I,L,B,w,D){let O=R/B,q=I/w,Y=R/2,J=I/2,H=L/2,te=B+1,k=w+1,se=0,_e=0,ae=new j;for(let V=0;V<k;V++){let ge=V*q-J;for(let Ye=0;Ye<te;Ye++){let $e=Ye*O-Y;ae[P]=$e*U,ae[b]=ge*z,ae[_]=H,f.push(ae.x,ae.y,ae.z),ae[P]=0,ae[b]=0,ae[_]=L>0?1:-1,g.push(ae.x,ae.y,ae.z),y.push(Ye/B),y.push(1-V/w),se+=1}}for(let V=0;V<w;V++)for(let ge=0;ge<B;ge++){let Ye=m+ge+te*V,$e=m+ge+te*(V+1),Ut=m+(ge+1)+te*(V+1),mt=m+(ge+1)+te*V;d.push(Ye,$e,mt),d.push($e,Ut,mt),_e+=6}h.addGroup(S,_e,D),S+=_e,m+=se}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new i(e.width,e.height,e.depth,e.widthSegments,e.heightSegments,e.depthSegments)}},Ss=class i extends Yt{constructor(e=1,t=1,n=4,s=8,o=1){super(),this.type="CapsuleGeometry",this.parameters={radius:e,height:t,capSegments:n,radialSegments:s,heightSegments:o},t=Math.max(0,t),n=Math.max(1,Math.floor(n)),s=Math.max(3,Math.floor(s)),o=Math.max(1,Math.floor(o));let l=[],h=[],d=[],f=[],g=t/2,y=Math.PI/2*e,m=t,S=2*y+m,T=n*2+o,P=s+1,b=new j,_=new j;for(let U=0;U<=T;U++){let z=0,R=0,I=0,L=0;if(U<=n){let D=U/n,O=D*Math.PI/2;R=-g-e*Math.cos(O),I=e*Math.sin(O),L=-e*Math.cos(O),z=D*y}else if(U<=n+o){let D=(U-n)/o;R=-g+D*t,I=e,L=0,z=y+D*m}else{let D=(U-n-o)/n,O=D*Math.PI/2;R=g+e*Math.sin(O),I=e*Math.cos(O),L=e*Math.sin(O),z=y+m+D*y}let B=Math.max(0,Math.min(1,z/S)),w=0;U===0?w=.5/s:U===T&&(w=-.5/s);for(let D=0;D<=s;D++){let O=D/s,q=O*Math.PI*2,Y=Math.sin(q),J=Math.cos(q);_.x=-I*J,_.y=R,_.z=I*Y,h.push(_.x,_.y,_.z),b.set(-I*J,L,I*Y),b.normalize(),d.push(b.x,b.y,b.z),f.push(O+w,B)}if(U>0){let D=(U-1)*P;for(let O=0;O<s;O++){let q=D+O,Y=D+O+1,J=U*P+O,H=U*P+O+1;l.push(q,Y,J),l.push(Y,H,J)}}}this.setIndex(l),this.setAttribute("position",new zt(h,3)),this.setAttribute("normal",new zt(d,3)),this.setAttribute("uv",new zt(f,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new i(e.radius,e.height,e.capSegments,e.radialSegments,e.heightSegments)}};var rr=class i extends Yt{constructor(e=1,t=1,n=1,s=32,o=1,l=!1,h=0,d=Math.PI*2){super(),this.type="CylinderGeometry",this.parameters={radiusTop:e,radiusBottom:t,height:n,radialSegments:s,heightSegments:o,openEnded:l,thetaStart:h,thetaLength:d};let f=this;s=Math.floor(s),o=Math.floor(o);let g=[],y=[],m=[],S=[],T=0,P=[],b=n/2,_=0;U(),l===!1&&(e>0&&z(!0),t>0&&z(!1)),this.setIndex(g),this.setAttribute("position",new zt(y,3)),this.setAttribute("normal",new zt(m,3)),this.setAttribute("uv",new zt(S,2));function U(){let R=new j,I=new j,L=0,B=(t-e)/n;for(let w=0;w<=o;w++){let D=[],O=w/o,q=O*(t-e)+e;for(let Y=0;Y<=s;Y++){let J=Y/s,H=J*d+h,te=Math.sin(H),k=Math.cos(H);I.x=q*te,I.y=-O*n+b,I.z=q*k,y.push(I.x,I.y,I.z),R.set(te,B,k).normalize(),m.push(R.x,R.y,R.z),S.push(J,1-O),D.push(T++)}P.push(D)}for(let w=0;w<s;w++)for(let D=0;D<o;D++){let O=P[D][w],q=P[D+1][w],Y=P[D+1][w+1],J=P[D][w+1];(e>0||D!==0)&&(g.push(O,q,J),L+=3),(t>0||D!==o-1)&&(g.push(q,Y,J),L+=3)}f.addGroup(_,L,0),_+=L}function z(R){let I=T,L=new nt,B=new j,w=0,D=R===!0?e:t,O=R===!0?1:-1;for(let Y=1;Y<=s;Y++)y.push(0,b*O,0),m.push(0,O,0),S.push(.5,.5),T++;let q=T;for(let Y=0;Y<=s;Y++){let H=Y/s*d+h,te=Math.cos(H),k=Math.sin(H);B.x=D*k,B.y=b*O,B.z=D*te,y.push(B.x,B.y,B.z),m.push(0,O,0),L.x=te*.5+.5,L.y=k*.5*O+.5,S.push(L.x,L.y),T++}for(let Y=0;Y<s;Y++){let J=I+Y,H=q+Y;R===!0?g.push(H,H+1,J):g.push(H+1,H,J),w+=3}f.addGroup(_,w,R===!0?1:2),_+=w}}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new i(e.radiusTop,e.radiusBottom,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}},eo=class i extends rr{constructor(e=1,t=1,n=32,s=1,o=!1,l=0,h=Math.PI*2){super(0,e,t,n,s,o,l,h),this.type="ConeGeometry",this.parameters={radius:e,height:t,radialSegments:n,heightSegments:s,openEnded:o,thetaStart:l,thetaLength:h}}static fromJSON(e){return new i(e.radius,e.height,e.radialSegments,e.heightSegments,e.openEnded,e.thetaStart,e.thetaLength)}};var sr=class i extends Yt{constructor(e=1,t=1,n=1,s=1){super(),this.type="PlaneGeometry",this.parameters={width:e,height:t,widthSegments:n,heightSegments:s};let o=e/2,l=t/2,h=Math.floor(n),d=Math.floor(s),f=h+1,g=d+1,y=e/h,m=t/d,S=[],T=[],P=[],b=[];for(let _=0;_<g;_++){let U=_*m-l;for(let z=0;z<f;z++){let R=z*y-o;T.push(R,-U,0),P.push(0,0,1),b.push(z/h),b.push(1-_/d)}}for(let _=0;_<d;_++)for(let U=0;U<h;U++){let z=U+f*_,R=U+f*(_+1),I=U+1+f*(_+1),L=U+1+f*_;S.push(z,R,L),S.push(R,I,L)}this.setIndex(S),this.setAttribute("position",new zt(T,3)),this.setAttribute("normal",new zt(P,3)),this.setAttribute("uv",new zt(b,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new i(e.width,e.height,e.widthSegments,e.heightSegments)}};var zr=class i extends Yt{constructor(e=1,t=32,n=16,s=0,o=Math.PI*2,l=0,h=Math.PI){super(),this.type="SphereGeometry",this.parameters={radius:e,widthSegments:t,heightSegments:n,phiStart:s,phiLength:o,thetaStart:l,thetaLength:h},t=Math.max(3,Math.floor(t)),n=Math.max(2,Math.floor(n));let d=Math.min(l+h,Math.PI),f=0,g=[],y=new j,m=new j,S=[],T=[],P=[],b=[];for(let _=0;_<=n;_++){let U=[],z=_/n,R=l+z*h,I=e*Math.cos(R),L=Math.sqrt(e*e-I*I),B=0;_===0&&l===0?B=.5/t:_===n&&d===Math.PI&&(B=-.5/t);for(let w=0;w<=t;w++){let D=w/t,O=s+D*o;y.x=-L*Math.cos(O),y.y=I,y.z=L*Math.sin(O),T.push(y.x,y.y,y.z),m.copy(y).normalize(),P.push(m.x,m.y,m.z),b.push(D+B,1-z),U.push(f++)}g.push(U)}for(let _=0;_<n;_++)for(let U=0;U<t;U++){let z=g[_][U+1],R=g[_][U],I=g[_+1][U],L=g[_+1][U+1];(_!==0||l>0)&&S.push(z,R,L),(_!==n-1||d<Math.PI)&&S.push(R,I,L)}this.setIndex(S),this.setAttribute("position",new zt(T,3)),this.setAttribute("normal",new zt(P,3)),this.setAttribute("uv",new zt(b,2))}copy(e){return super.copy(e),this.parameters=Object.assign({},e.parameters),this}static fromJSON(e){return new i(e.radius,e.widthSegments,e.heightSegments,e.phiStart,e.phiLength,e.thetaStart,e.thetaLength)}};function lr(i){let e={};for(let t in i){e[t]={};for(let n in i[t]){let s=i[t][n];if(hu(s))s.isRenderTargetTexture?(et("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),e[t][n]=null):e[t][n]=s.clone();else if(Array.isArray(s))if(hu(s[0])){let o=[];for(let l=0,h=s.length;l<h;l++)o[l]=s[l].clone();e[t][n]=o}else e[t][n]=s.slice();else e[t][n]=s}}return e}function pn(i){let e={};for(let t=0;t<i.length;t++){let n=lr(i[t]);for(let s in n)e[s]=n[s]}return e}function hu(i){return i&&(i.isColor||i.isMatrix3||i.isMatrix4||i.isVector2||i.isVector3||i.isVector4||i.isTexture||i.isQuaternion)}function N0(i){let e=[];for(let t=0;t<i.length;t++)e.push(i[t].clone());return e}function Nc(i){let e=i.getRenderTarget();return e===null?i.outputColorSpace:e.isXRRenderTarget===!0?e.texture.colorSpace:xt.workingColorSpace}var rd={clone:lr,merge:pn},U0=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,O0=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`,Dn=class extends Si{constructor(e){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=U0,this.fragmentShader=O0,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,e!==void 0&&this.setValues(e)}copy(e){return super.copy(e),this.fragmentShader=e.fragmentShader,this.vertexShader=e.vertexShader,this.uniforms=lr(e.uniforms),this.uniformsGroups=N0(e.uniformsGroups),this.defines=Object.assign({},e.defines),this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.fog=e.fog,this.lights=e.lights,this.clipping=e.clipping,this.extensions=Object.assign({},e.extensions),this.glslVersion=e.glslVersion,this.defaultAttributeValues=Object.assign({},e.defaultAttributeValues),this.index0AttributeName=e.index0AttributeName,this.uniformsNeedUpdate=e.uniformsNeedUpdate,this}toJSON(e){let t=super.toJSON(e);t.glslVersion=this.glslVersion,t.uniforms={};for(let s in this.uniforms){let l=this.uniforms[s].value;l&&l.isTexture?t.uniforms[s]={type:"t",value:l.toJSON(e).uuid}:l&&l.isColor?t.uniforms[s]={type:"c",value:l.getHex()}:l&&l.isVector2?t.uniforms[s]={type:"v2",value:l.toArray()}:l&&l.isVector3?t.uniforms[s]={type:"v3",value:l.toArray()}:l&&l.isVector4?t.uniforms[s]={type:"v4",value:l.toArray()}:l&&l.isMatrix3?t.uniforms[s]={type:"m3",value:l.toArray()}:l&&l.isMatrix4?t.uniforms[s]={type:"m4",value:l.toArray()}:t.uniforms[s]={value:l}}Object.keys(this.defines).length>0&&(t.defines=this.defines),t.vertexShader=this.vertexShader,t.fragmentShader=this.fragmentShader,t.lights=this.lights,t.clipping=this.clipping;let n={};for(let s in this.extensions)this.extensions[s]===!0&&(n[s]=!0);return Object.keys(n).length>0&&(t.extensions=n),t}fromJSON(e,t){if(super.fromJSON(e,t),e.uniforms!==void 0)for(let n in e.uniforms){let s=e.uniforms[n];switch(this.uniforms[n]={},s.type){case"t":this.uniforms[n].value=t[s.value]||null;break;case"c":this.uniforms[n].value=new ht().setHex(s.value);break;case"v2":this.uniforms[n].value=new nt().fromArray(s.value);break;case"v3":this.uniforms[n].value=new j().fromArray(s.value);break;case"v4":this.uniforms[n].value=new Ht().fromArray(s.value);break;case"m3":this.uniforms[n].value=new at().fromArray(s.value);break;case"m4":this.uniforms[n].value=new Ot().fromArray(s.value);break;default:this.uniforms[n].value=s.value}}if(e.defines!==void 0&&(this.defines=e.defines),e.vertexShader!==void 0&&(this.vertexShader=e.vertexShader),e.fragmentShader!==void 0&&(this.fragmentShader=e.fragmentShader),e.glslVersion!==void 0&&(this.glslVersion=e.glslVersion),e.extensions!==void 0)for(let n in e.extensions)this.extensions[n]=e.extensions[n];return e.lights!==void 0&&(this.lights=e.lights),e.clipping!==void 0&&(this.clipping=e.clipping),this}},to=class extends Dn{constructor(e){super(e),this.isRawShaderMaterial=!0,this.type="RawShaderMaterial"}};var bs=class extends Si{constructor(e){super(),this.isMeshPhongMaterial=!0,this.type="MeshPhongMaterial",this.color=new ht(16777215),this.specular=new ht(1118481),this.shininess=30,this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.emissive=new ht(0),this.emissiveIntensity=1,this.emissiveMap=null,this.bumpMap=null,this.bumpScale=1,this.normalMap=null,this.normalMapType=rl,this.normalScale=new nt(1,1),this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new xi,this.combine=vo,this.reflectivity=1,this.envMapIntensity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.flatShading=!1,this.fog=!0,this.setValues(e)}copy(e){return super.copy(e),this.color.copy(e.color),this.specular.copy(e.specular),this.shininess=e.shininess,this.map=e.map,this.lightMap=e.lightMap,this.lightMapIntensity=e.lightMapIntensity,this.aoMap=e.aoMap,this.aoMapIntensity=e.aoMapIntensity,this.emissive.copy(e.emissive),this.emissiveMap=e.emissiveMap,this.emissiveIntensity=e.emissiveIntensity,this.bumpMap=e.bumpMap,this.bumpScale=e.bumpScale,this.normalMap=e.normalMap,this.normalMapType=e.normalMapType,this.normalScale.copy(e.normalScale),this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.specularMap=e.specularMap,this.alphaMap=e.alphaMap,this.envMap=e.envMap,this.envMapRotation.copy(e.envMapRotation),this.combine=e.combine,this.reflectivity=e.reflectivity,this.envMapIntensity=e.envMapIntensity,this.refractionRatio=e.refractionRatio,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this.wireframeLinecap=e.wireframeLinecap,this.wireframeLinejoin=e.wireframeLinejoin,this.flatShading=e.flatShading,this.fog=e.fog,this}};var no=class extends Si{constructor(e){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=Hu,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(e)}copy(e){return super.copy(e),this.depthPacking=e.depthPacking,this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this.wireframe=e.wireframe,this.wireframeLinewidth=e.wireframeLinewidth,this}},io=class extends Si{constructor(e){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(e)}copy(e){return super.copy(e),this.map=e.map,this.alphaMap=e.alphaMap,this.displacementMap=e.displacementMap,this.displacementScale=e.displacementScale,this.displacementBias=e.displacementBias,this}};function wr(i,e){return!i||i.constructor===e?i:typeof e.BYTES_PER_ELEMENT=="number"?new e(i):Array.prototype.slice.call(i)}function Ql(i){return i!==void 0&&i.inTangents!==void 0&&i.outTangents!==void 0}var Ni=class{constructor(e,t,n,s){this.parameterPositions=e,this._cachedIndex=0,this.resultBuffer=s!==void 0?s:new t.constructor(n),this.sampleValues=t,this.valueSize=n,this.settings=null,this.DefaultSettings_={}}evaluate(e){let t=this.parameterPositions,n=this._cachedIndex,s=t[n],o=t[n-1];e:{t:{let l;n:{i:if(!(e<s)){for(let h=n+2;;){if(s===void 0){if(e<o)break i;return n=t.length,this._cachedIndex=n,this.copySampleValue_(n-1)}if(n===h)break;if(o=s,s=t[++n],e<s)break t}l=t.length;break n}if(!(e>=o)){let h=t[1];e<h&&(n=2,o=h);for(let d=n-2;;){if(o===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(n===d)break;if(s=o,o=t[--n-1],e>=o)break t}l=n,n=0;break n}break e}for(;n<l;){let h=n+l>>>1;e<t[h]?l=h:n=h+1}if(s=t[n],o=t[n-1],o===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(s===void 0)return n=t.length,this._cachedIndex=n,this.copySampleValue_(n-1)}this._cachedIndex=n,this.intervalChanged_(n,o,s)}return this.interpolate_(n,o,e,s)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(e){let t=this.resultBuffer,n=this.sampleValues,s=this.valueSize,o=e*s;for(let l=0;l!==s;++l)t[l]=n[o+l];return t}interpolate_(){throw new Error("THREE.Interpolant: Call to abstract method.")}intervalChanged_(){}},ro=class extends Ni{constructor(e,t,n,s){super(e,t,n,s),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:ic,endingEnd:ic}}intervalChanged_(e,t,n){let s=this.parameterPositions,o=e-2,l=e+1,h=s[o],d=s[l];if(h===void 0)switch(this.getSettings_().endingStart){case rc:o=e,h=2*t-n;break;case sc:o=s.length-2,h=t+s[o]-s[o+1];break;default:o=e,h=n}if(d===void 0)switch(this.getSettings_().endingEnd){case rc:l=e,d=2*n-t;break;case sc:l=1,d=n+s[1]-s[0];break;default:l=e-1,d=t}let f=(n-t)*.5,g=this.valueSize;this._weightPrev=f/(t-h),this._weightNext=f/(d-n),this._offsetPrev=o*g,this._offsetNext=l*g}interpolate_(e,t,n,s){let o=this.resultBuffer,l=this.sampleValues,h=this.valueSize,d=e*h,f=d-h,g=this._offsetPrev,y=this._offsetNext,m=this._weightPrev,S=this._weightNext,T=(n-t)/(s-t),P=T*T,b=P*T,_=-m*b+2*m*P-m*T,U=(1+m)*b+(-1.5-2*m)*P+(-.5+m)*T+1,z=(-1-S)*b+(1.5+S)*P+.5*T,R=S*b-S*P;for(let I=0;I!==h;++I)o[I]=_*l[g+I]+U*l[f+I]+z*l[d+I]+R*l[y+I];return o}},so=class extends Ni{constructor(e,t,n,s){super(e,t,n,s)}interpolate_(e,t,n,s){let o=this.resultBuffer,l=this.sampleValues,h=this.valueSize,d=e*h,f=d-h,g=(n-t)/(s-t),y=1-g;for(let m=0;m!==h;++m)o[m]=l[f+m]*y+l[d+m]*g;return o}},ao=class extends Ni{constructor(e,t,n,s){super(e,t,n,s)}interpolate_(e){return this.copySampleValue_(e-1)}},oo=class extends Ni{interpolate_(e,t,n,s){let o=this.resultBuffer,l=this.sampleValues,h=this.valueSize,d=e*h,f=d-h,g=this.inTangents,y=this.outTangents;if(!g||!y){let T=(n-t)/(s-t),P=1-T;for(let b=0;b!==h;++b)o[b]=l[f+b]*P+l[d+b]*T;return o}let m=h*2,S=e-1;for(let T=0;T!==h;++T){let P=l[f+T],b=l[d+T],_=S*m+T*2,U=y[_],z=y[_+1],R=e*m+T*2,I=g[R],L=g[R+1],B=k0(n,t,U,I,s);o[T]=sd(B,P,z,L,b)}return o}};function sd(i,e,t,n,s){let o=1-i;return o*o*o*e+3*o*o*i*t+3*o*i*i*n+i*i*i*s}function B0(i,e,t,n,s){let o=1-i;return 3*o*o*(t-e)+6*o*i*(n-t)+3*i*i*(s-n)}function k0(i,e,t,n,s){let o=(i-e)/(s-e);for(let l=0;l<8;l++){let h=sd(o,e,t,n,s)-i;if(Math.abs(h)<1e-10)break;let d=B0(o,e,t,n,s);if(Math.abs(d)<1e-10)break;o=Math.max(0,Math.min(1,o-h/d))}return o}var Ln=class{constructor(e,t,n,s){if(e===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(t===void 0||t.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+e);this.name=e,this.times=wr(t,this.TimeBufferType),this.values=wr(n,this.ValueBufferType),this.setInterpolation(s||this.DefaultInterpolation)}static toJSON(e){let t=e.constructor,n;if(t.toJSON!==this.toJSON)n=t.toJSON(e);else{n={name:e.name,times:wr(e.times,Array),values:wr(e.values,Array)};let s=e.getInterpolation();s!==e.DefaultInterpolation&&(n.interpolation=s),Ql(e.settings)&&(n.settings={inTangents:wr(e.settings.inTangents,Array),outTangents:wr(e.settings.outTangents,Array)})}return n.type=e.ValueTypeName,n}InterpolantFactoryMethodDiscrete(e){return new ao(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodLinear(e){return new so(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodSmooth(e){return new ro(this.times,this.values,this.getValueSize(),e)}InterpolantFactoryMethodBezier(e){let t=new oo(this.times,this.values,this.getValueSize(),e);return this.settings&&(t.inTangents=this.settings.inTangents,t.outTangents=this.settings.outTangents),t}setInterpolation(e){let t;switch(e){case hs:t=this.InterpolantFactoryMethodDiscrete;break;case Xa:t=this.InterpolantFactoryMethodLinear;break;case Fa:t=this.InterpolantFactoryMethodSmooth;break;case nc:t=this.InterpolantFactoryMethodBezier;break}if(t===void 0){let n="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(e!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(n);return et("KeyframeTrack:",n),this}return this.createInterpolant=t,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return hs;case this.InterpolantFactoryMethodLinear:return Xa;case this.InterpolantFactoryMethodSmooth:return Fa;case this.InterpolantFactoryMethodBezier:return nc}}getValueSize(){return this.values.length/this.times.length}shift(e){if(e!==0){let t=this.times;for(let n=0,s=t.length;n!==s;++n)t[n]+=e}return this}scale(e){if(e!==1){let t=this.times;for(let n=0,s=t.length;n!==s;++n)t[n]*=e;Ql(this.settings)&&(uu(this.settings.inTangents,e),uu(this.settings.outTangents,e))}return this}trim(e,t){let n=this.times,s=n.length,o=0,l=s-1;for(;o!==s&&n[o]<e;)++o;for(;l!==-1&&n[l]>t;)--l;if(++l,o!==0||l!==s){o>=l&&(l=Math.max(l,1),o=l-1);let h=this.getValueSize();this.times=n.slice(o,l),this.values=this.values.slice(o*h,l*h)}return this}validate(){let e=!0,t=this.getValueSize();t-Math.floor(t)!==0&&(it("KeyframeTrack: Invalid value size in track.",this),e=!1);let n=this.times,s=this.values,o=n.length;o===0&&(it("KeyframeTrack: Track is empty.",this),e=!1);let l=null;for(let h=0;h!==o;h++){let d=n[h];if(typeof d=="number"&&isNaN(d)){it("KeyframeTrack: Time is not a valid number.",this,h,d),e=!1;break}if(l!==null&&l>d){it("KeyframeTrack: Out of order keys.",this,h,d,l),e=!1;break}l=d}if(s!==void 0&&e0(s))for(let h=0,d=s.length;h!==d;++h){let f=s[h];if(isNaN(f)){it("KeyframeTrack: Value is not a valid number.",this,h,f),e=!1;break}}return e}optimize(){let e=this.times.slice(),t=this.values.slice(),n=this.getValueSize(),s=this.getInterpolation()===Fa,o=e.length-1,l=1;for(let h=1;h<o;++h){let d=!1,f=e[h],g=e[h+1];if(f!==g&&(h!==1||f!==e[0]))if(s)d=!0;else{let y=h*n,m=y-n,S=y+n;for(let T=0;T!==n;++T){let P=t[y+T];if(P!==t[m+T]||P!==t[S+T]){d=!0;break}}}if(d){if(h!==l){e[l]=e[h];let y=h*n,m=l*n;for(let S=0;S!==n;++S)t[m+S]=t[y+S]}++l}}if(o>0){e[l]=e[o];for(let h=o*n,d=l*n,f=0;f!==n;++f)t[d+f]=t[h+f];++l}return l!==e.length?(this.times=e.slice(0,l),this.values=t.slice(0,l*n)):(this.times=e,this.values=t),this}clone(){let e=this.times.slice(),t=this.values.slice(),n=this.constructor,s=new n(this.name,e,t);return s.createInterpolant=this.createInterpolant,Ql(this.settings)&&(s.settings={inTangents:this.settings.inTangents.slice(),outTangents:this.settings.outTangents.slice()}),s}};function uu(i,e){for(let t=0,n=i.length;t!==n;t+=2)i[t]*=e}Ln.prototype.ValueTypeName="";Ln.prototype.TimeBufferType=Float32Array;Ln.prototype.ValueBufferType=Float32Array;Ln.prototype.DefaultInterpolation=Xa;var Ui=class extends Ln{constructor(e,t,n){super(e,t,n)}};Ui.prototype.ValueTypeName="bool";Ui.prototype.ValueBufferType=Array;Ui.prototype.DefaultInterpolation=hs;Ui.prototype.InterpolantFactoryMethodLinear=void 0;Ui.prototype.InterpolantFactoryMethodSmooth=void 0;var lo=class extends Ln{constructor(e,t,n,s){super(e,t,n,s)}};lo.prototype.ValueTypeName="color";var co=class extends Ln{constructor(e,t,n,s){super(e,t,n,s)}};co.prototype.ValueTypeName="number";var ho=class extends Ni{constructor(e,t,n,s){super(e,t,n,s)}interpolate_(e,t,n,s){let o=this.resultBuffer,l=this.sampleValues,h=this.valueSize,d=(n-t)/(s-t),f=e*h;for(let g=f+h;f!==g;f+=4)In.slerpFlat(o,0,l,f-h,l,f,d);return o}},Ms=class extends Ln{constructor(e,t,n,s){super(e,t,n,s)}InterpolantFactoryMethodLinear(e){return new ho(this.times,this.values,this.getValueSize(),e)}};Ms.prototype.ValueTypeName="quaternion";Ms.prototype.InterpolantFactoryMethodSmooth=void 0;var Oi=class extends Ln{constructor(e,t,n){super(e,t,n)}};Oi.prototype.ValueTypeName="string";Oi.prototype.ValueBufferType=Array;Oi.prototype.DefaultInterpolation=hs;Oi.prototype.InterpolantFactoryMethodLinear=void 0;Oi.prototype.InterpolantFactoryMethodSmooth=void 0;var uo=class extends Ln{constructor(e,t,n,s){super(e,t,n,s)}};uo.prototype.ValueTypeName="vector";var fo=class{constructor(e,t,n){let s=this,o=!1,l=0,h=0,d,f=[];this.onStart=void 0,this.onLoad=e,this.onProgress=t,this.onError=n,this._abortController=null,this.itemStart=function(g){h++,o===!1&&s.onStart!==void 0&&s.onStart(g,l,h),o=!0},this.itemEnd=function(g){l++,s.onProgress!==void 0&&s.onProgress(g,l,h),l===h&&(o=!1,s.onLoad!==void 0&&s.onLoad())},this.itemError=function(g){s.onError!==void 0&&s.onError(g)},this.resolveURL=function(g){return g=g.normalize("NFC"),d?d(g):g},this.setURLModifier=function(g){return d=g,this},this.addHandler=function(g,y){return f.push(g,y),this},this.removeHandler=function(g){let y=f.indexOf(g);return y!==-1&&f.splice(y,2),this},this.getHandler=function(g){for(let y=0,m=f.length;y<m;y+=2){let S=f[y],T=f[y+1];if(S.global&&(S.lastIndex=0),S.test(g))return T}return null},this.abort=function(){return this.abortController.abort(),this._abortController=null,this}}get abortController(){return this._abortController||(this._abortController=new AbortController),this._abortController}},ad=new fo,po=class{constructor(e){this.manager=e!==void 0?e:ad,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}load(){}loadAsync(e,t){let n=this;return new Promise(function(s,o){n.load(e,s,t,o)})}parse(){}setCrossOrigin(e){return this.crossOrigin=e,this}setWithCredentials(e){return this.withCredentials=e,this}setPath(e){return this.path=e,this}setResourcePath(e){return this.resourcePath=e,this}setRequestHeader(e){return this.requestHeader=e,this}abort(){return this}};po.DEFAULT_MATERIAL_NAME="__DEFAULT";var Es=class extends on{constructor(e,t=1){super(),this.isLight=!0,this.type="Light",this.color=new ht(e),this.intensity=t}copy(e,t){return super.copy(e,t),this.color.copy(e.color),this.intensity=e.intensity,this}toJSON(e){let t=super.toJSON(e);return t.object.color=this.color.getHex(),t.object.intensity=this.intensity,t}},ws=class extends Es{constructor(e,t,n){super(e,n),this.isHemisphereLight=!0,this.type="HemisphereLight",this.position.copy(on.DEFAULT_UP),this.updateMatrix(),this.groundColor=new ht(t)}copy(e,t){return super.copy(e,t),this.groundColor.copy(e.groundColor),this}toJSON(e){let t=super.toJSON(e);return t.object.groundColor=this.groundColor.getHex(),t}},ec=new Ot,du=new j,fu=new j,mo=class{constructor(e){this.camera=e,this.intensity=1,this.bias=0,this.biasNode=null,this.normalBias=0,this.radius=1,this.blurSamples=8,this.mapSize=new nt(512,512),this.mapType=En,this.map=null,this.mapPass=null,this.matrix=new Ot,this.autoUpdate=!0,this.needsUpdate=!1,this._frustum=new Br,this._frameExtents=new nt(1,1),this._viewportCount=1,this._viewports=[new Ht(0,0,1,1)]}getViewportCount(){return this._viewportCount}getCamera(){return this.camera}getFrustum(){return this._frustum}updateMatrices(e){let t=this.camera;du.setFromMatrixPosition(e.matrixWorld),t.position.copy(du),fu.setFromMatrixPosition(e.target.matrixWorld),t.lookAt(fu),t.updateMatrixWorld(),this._updateMatrix(t,this.matrix,this._frustum)}_updateMatrix(e,t,n,s){ec.multiplyMatrices(e.projectionMatrix,e.matrixWorldInverse),n.setFromProjectionMatrix(ec,e.coordinateSystem,e.reversedDepth);let o=this._frameExtents,l=s?s.z/o.x:1,h=s?s.w/o.y:1,d=s?s.x/o.x:0,f=s?s.y/o.y:0;e.coordinateSystem===Ir||e.reversedDepth?t.set(.5*l,0,0,.5*l+d,0,.5*h,0,.5*h+f,0,0,1,0,0,0,0,1):t.set(.5*l,0,0,.5*l+d,0,.5*h,0,.5*h+f,0,0,.5,.5,0,0,0,1),t.multiply(ec)}getViewport(e){return this._viewports[e]}getFrameExtents(){return this._frameExtents}dispose(){this.map&&this.map.dispose(),this.mapPass&&this.mapPass.dispose()}copy(e){return this.camera=e.camera.clone(),this.intensity=e.intensity,this.bias=e.bias,this.radius=e.radius,this.autoUpdate=e.autoUpdate,this.needsUpdate=e.needsUpdate,this.normalBias=e.normalBias,this.blurSamples=e.blurSamples,this.mapSize.copy(e.mapSize),this.biasNode=e.biasNode,this}clone(){return new this.constructor().copy(this)}toJSON(){let e={};return e.intensity=this.intensity,e.bias=this.bias,e.normalBias=this.normalBias,e.radius=this.radius,e.blurSamples=this.blurSamples,e.mapSize=this.mapSize.toArray(),e.camera=this.camera.toJSON(!1).object,delete e.camera.matrix,e}},Ia=new j,Da=new In,ri=new j,Ts=class extends on{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new Ot,this.projectionMatrix=new Ot,this.projectionMatrixInverse=new Ot,this.coordinateSystem=Yn,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(e,t){return super.copy(e,t),this.matrixWorldInverse.copy(e.matrixWorldInverse),this.projectionMatrix.copy(e.projectionMatrix),this.projectionMatrixInverse.copy(e.projectionMatrixInverse),this.coordinateSystem=e.coordinateSystem,this}getWorldDirection(e){return super.getWorldDirection(e).negate()}updateMatrixWorld(e){super.updateMatrixWorld(e),this.matrixWorld.decompose(Ia,Da,ri),ri.x===1&&ri.y===1&&ri.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Ia,Da,ri.set(1,1,1)).invert()}updateWorldMatrix(e,t,n=!1){super.updateWorldMatrix(e,t,n),this.matrixWorld.decompose(Ia,Da,ri),ri.x===1&&ri.y===1&&ri.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Ia,Da,ri.set(1,1,1)).invert()}clone(){return new this.constructor().copy(this)}},Pi=new j,pu=new nt,mu=new nt,fn=class extends Ts{constructor(e=50,t=1,n=.1,s=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=e,this.zoom=1,this.near=n,this.far=s,this.focus=10,this.aspect=t,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.fov=e.fov,this.zoom=e.zoom,this.near=e.near,this.far=e.far,this.focus=e.focus,this.aspect=e.aspect,this.view=e.view===null?null:Object.assign({},e.view),this.filmGauge=e.filmGauge,this.filmOffset=e.filmOffset,this}setFocalLength(e){let t=.5*this.getFilmHeight()/e;this.fov=Lr*2*Math.atan(t),this.updateProjectionMatrix()}getFocalLength(){let e=Math.tan(ls*.5*this.fov);return .5*this.getFilmHeight()/e}getEffectiveFOV(){return Lr*2*Math.atan(Math.tan(ls*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(e,t,n){Pi.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),t.set(Pi.x,Pi.y).multiplyScalar(-e/Pi.z),Pi.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),n.set(Pi.x,Pi.y).multiplyScalar(-e/Pi.z)}getViewSize(e,t){return this.getViewBounds(e,pu,mu),t.subVectors(mu,pu)}setViewOffset(e,t,n,s,o,l){this.aspect=e/t,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=n,this.view.offsetY=s,this.view.width=o,this.view.height=l,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=this.near,t=e*Math.tan(ls*.5*this.fov)/this.zoom,n=2*t,s=this.aspect*n,o=-.5*s,l=this.view;if(this.view!==null&&this.view.enabled){let d=l.fullWidth,f=l.fullHeight;o+=l.offsetX*s/d,t-=l.offsetY*n/f,s*=l.width/d,n*=l.height/f}let h=this.filmOffset;h!==0&&(o+=e*h/this.getFilmWidth()),this.projectionMatrix.makePerspective(o,o+s,t,t-n,e,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.fov=this.fov,t.object.zoom=this.zoom,t.object.near=this.near,t.object.far=this.far,t.object.focus=this.focus,t.object.aspect=this.aspect,this.view!==null&&(t.object.view=Object.assign({},this.view)),t.object.filmGauge=this.filmGauge,t.object.filmOffset=this.filmOffset,t}};var Vr=class extends Ts{constructor(e=-1,t=1,n=1,s=-1,o=.1,l=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=e,this.right=t,this.top=n,this.bottom=s,this.near=o,this.far=l,this.updateProjectionMatrix()}copy(e,t){return super.copy(e,t),this.left=e.left,this.right=e.right,this.top=e.top,this.bottom=e.bottom,this.near=e.near,this.far=e.far,this.zoom=e.zoom,this.view=e.view===null?null:Object.assign({},e.view),this}setViewOffset(e,t,n,s,o,l){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=e,this.view.fullHeight=t,this.view.offsetX=n,this.view.offsetY=s,this.view.width=o,this.view.height=l,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let e=(this.right-this.left)/(2*this.zoom),t=(this.top-this.bottom)/(2*this.zoom),n=(this.right+this.left)/2,s=(this.top+this.bottom)/2,o=n-e,l=n+e,h=s+t,d=s-t;if(this.view!==null&&this.view.enabled){let f=(this.right-this.left)/this.view.fullWidth/this.zoom,g=(this.top-this.bottom)/this.view.fullHeight/this.zoom;o+=f*this.view.offsetX,l=o+f*this.view.width,h-=g*this.view.offsetY,d=h-g*this.view.height}this.projectionMatrix.makeOrthographic(o,l,h,d,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(e){let t=super.toJSON(e);return t.object.zoom=this.zoom,t.object.left=this.left,t.object.right=this.right,t.object.top=this.top,t.object.bottom=this.bottom,t.object.near=this.near,t.object.far=this.far,this.view!==null&&(t.object.view=Object.assign({},this.view)),t}},ac=class extends mo{constructor(){super(new Vr(-5,5,5,-5,.5,500)),this.isDirectionalLightShadow=!0}},As=class extends Es{constructor(e,t){super(e,t),this.isDirectionalLight=!0,this.type="DirectionalLight",this.position.copy(on.DEFAULT_UP),this.updateMatrix(),this.target=new on,this.shadow=new ac}dispose(){super.dispose(),this.shadow.dispose()}copy(e){return super.copy(e),this.target=e.target.clone(),this.shadow=e.shadow.clone(),this}toJSON(e){let t=super.toJSON(e);return t.object.shadow=this.shadow.toJSON(),t.object.target=this.target.uuid,t}};var Tr=-90,Ar=1,go=class extends on{constructor(e,t,n){super(),this.type="CubeCamera",this.renderTarget=n,this.coordinateSystem=null,this.activeMipmapLevel=0;let s=new fn(Tr,Ar,e,t);s.layers=this.layers,this.add(s);let o=new fn(Tr,Ar,e,t);o.layers=this.layers,this.add(o);let l=new fn(Tr,Ar,e,t);l.layers=this.layers,this.add(l);let h=new fn(Tr,Ar,e,t);h.layers=this.layers,this.add(h);let d=new fn(Tr,Ar,e,t);d.layers=this.layers,this.add(d);let f=new fn(Tr,Ar,e,t);f.layers=this.layers,this.add(f)}updateCoordinateSystem(){let e=this.coordinateSystem,t=this.children.concat(),[n,s,o,l,h,d]=t;for(let f of t)this.remove(f);if(e===Yn)n.up.set(0,1,0),n.lookAt(1,0,0),s.up.set(0,1,0),s.lookAt(-1,0,0),o.up.set(0,0,-1),o.lookAt(0,1,0),l.up.set(0,0,1),l.lookAt(0,-1,0),h.up.set(0,1,0),h.lookAt(0,0,1),d.up.set(0,1,0),d.lookAt(0,0,-1);else if(e===Ir)n.up.set(0,-1,0),n.lookAt(-1,0,0),s.up.set(0,-1,0),s.lookAt(1,0,0),o.up.set(0,0,1),o.lookAt(0,1,0),l.up.set(0,0,-1),l.lookAt(0,-1,0),h.up.set(0,-1,0),h.lookAt(0,0,1),d.up.set(0,-1,0),d.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+e);for(let f of t)this.add(f),f.updateMatrixWorld()}update(e,t){this.parent===null&&this.updateMatrixWorld();let{renderTarget:n,activeMipmapLevel:s}=this;this.coordinateSystem!==e.coordinateSystem&&(this.coordinateSystem=e.coordinateSystem,this.updateCoordinateSystem());let[o,l,h,d,f,g]=this.children,y=e.getRenderTarget(),m=e.getActiveCubeFace(),S=e.getActiveMipmapLevel(),T=e.xr.enabled;e.xr.enabled=!1;let P=n.texture.generateMipmaps;n.texture.generateMipmaps=!1;let b=!1;e.isWebGLRenderer===!0?b=e.state.buffers.depth.getReversed():b=e.reversedDepthBuffer,e.setRenderTarget(n,0,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,o),e.setRenderTarget(n,1,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,l),e.setRenderTarget(n,2,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,h),e.setRenderTarget(n,3,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,d),e.setRenderTarget(n,4,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,f),n.texture.generateMipmaps=P,e.setRenderTarget(n,5,s),b&&e.autoClear===!1&&e.clearDepth(),e.render(t,g),e.setRenderTarget(y,m,S),e.xr.enabled=T,n.texture.needsPMREMUpdate=!0}},_o=class extends fn{constructor(e=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=e}};var Uc="\\[\\]\\.:\\/",z0=new RegExp("["+Uc+"]","g"),Oc="[^"+Uc+"]",V0="[^"+Uc.replace("\\.","")+"]",G0=/((?:WC+[\/:])*)/.source.replace("WC",Oc),H0=/(WCOD+)?/.source.replace("WCOD",V0),W0=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",Oc),X0=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",Oc),$0=new RegExp("^"+G0+H0+W0+X0+"$"),j0=["material","materials","bones","map"],oc=class{constructor(e,t,n){let s=n||Gt.parseTrackName(t);this._targetGroup=e,this._bindings=e.subscribe_(t,s)}getValue(e,t){this.bind();let n=this._targetGroup.nCachedObjects_,s=this._bindings[n];s!==void 0&&s.getValue(e,t)}setValue(e,t){let n=this._bindings;for(let s=this._targetGroup.nCachedObjects_,o=n.length;s!==o;++s)n[s].setValue(e,t)}bind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,n=e.length;t!==n;++t)e[t].bind()}unbind(){let e=this._bindings;for(let t=this._targetGroup.nCachedObjects_,n=e.length;t!==n;++t)e[t].unbind()}},Gt=class i{constructor(e,t,n){this.path=t,this.parsedPath=n||i.parseTrackName(t),this.node=i.findNode(e,this.parsedPath.nodeName),this.rootNode=e,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(e,t,n){return e&&e.isAnimationObjectGroup?new i.Composite(e,t,n):new i(e,t,n)}static sanitizeNodeName(e){return e.replace(/\s/g,"_").replace(z0,"")}static parseTrackName(e){let t=$0.exec(e);if(t===null)throw new Error("THREE.PropertyBinding: Cannot parse trackName: "+e);let n={nodeName:t[2],objectName:t[3],objectIndex:t[4],propertyName:t[5],propertyIndex:t[6]},s=n.nodeName&&n.nodeName.lastIndexOf(".");if(s!==void 0&&s!==-1){let o=n.nodeName.substring(s+1);j0.indexOf(o)!==-1&&(n.nodeName=n.nodeName.substring(0,s),n.objectName=o)}if(n.propertyName===null||n.propertyName.length===0)throw new Error("THREE.PropertyBinding: can not parse propertyName from trackName: "+e);return n}static findNode(e,t){if(t===void 0||t===""||t==="."||t===-1||t===e.name||t===e.uuid)return e;if(e.skeleton){let n=e.skeleton.getBoneByName(t);if(n!==void 0)return n}if(e.children){let n=function(o){for(let l=0;l<o.length;l++){let h=o[l];if(h.name===t||h.uuid===t)return h;let d=n(h.children);if(d)return d}return null},s=n(e.children);if(s)return s}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(e,t){e[t]=this.targetObject[this.propertyName]}_getValue_array(e,t){let n=this.resolvedProperty;for(let s=0,o=n.length;s!==o;++s)e[t++]=n[s]}_getValue_arrayElement(e,t){e[t]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(e,t){this.resolvedProperty.toArray(e,t)}_setValue_direct(e,t){this.targetObject[this.propertyName]=e[t]}_setValue_direct_setNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(e,t){this.targetObject[this.propertyName]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(e,t){let n=this.resolvedProperty;for(let s=0,o=n.length;s!==o;++s)n[s]=e[t++]}_setValue_array_setNeedsUpdate(e,t){let n=this.resolvedProperty;for(let s=0,o=n.length;s!==o;++s)n[s]=e[t++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(e,t){let n=this.resolvedProperty;for(let s=0,o=n.length;s!==o;++s)n[s]=e[t++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(e,t){this.resolvedProperty[this.propertyIndex]=e[t]}_setValue_arrayElement_setNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty[this.propertyIndex]=e[t],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(e,t){this.resolvedProperty.fromArray(e,t)}_setValue_fromArray_setNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(e,t){this.resolvedProperty.fromArray(e,t),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(e,t){this.bind(),this.getValue(e,t)}_setValue_unbound(e,t){this.bind(),this.setValue(e,t)}bind(){let e=this.node,t=this.parsedPath,n=t.objectName,s=t.propertyName,o=t.propertyIndex;if(e||(e=i.findNode(this.rootNode,t.nodeName),this.node=e),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!e){et("PropertyBinding: No target node found for track: "+this.path+".");return}if(n){let f=t.objectIndex;switch(n){case"materials":if(!e.material){it("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.materials){it("PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}e=e.material.materials;break;case"bones":if(!e.skeleton){it("PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}e=e.skeleton.bones;for(let g=0;g<e.length;g++)if(e[g].name===f){f=g;break}break;case"map":if("map"in e){e=e.map;break}if(!e.material){it("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!e.material.map){it("PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}e=e.material.map;break;default:if(e[n]===void 0){it("PropertyBinding: Can not bind to objectName of node undefined.",this);return}e=e[n]}if(f!==void 0){if(e[f]===void 0){it("PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,e);return}e=e[f]}}let l=e[s];if(l===void 0){let f=t.nodeName;it("PropertyBinding: Trying to update property for track: "+f+"."+s+" but it wasn't found.",e);return}let h=this.Versioning.None;this.targetObject=e,e.isMaterial===!0?h=this.Versioning.NeedsUpdate:e.isObject3D===!0&&(h=this.Versioning.MatrixWorldNeedsUpdate);let d=this.BindingType.Direct;if(o!==void 0){if(s==="morphTargetInfluences"){if(!e.geometry){it("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!e.geometry.morphAttributes){it("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}e.morphTargetDictionary[o]!==void 0&&(o=e.morphTargetDictionary[o])}d=this.BindingType.ArrayElement,this.resolvedProperty=l,this.propertyIndex=o}else l.fromArray!==void 0&&l.toArray!==void 0?(d=this.BindingType.HasFromToArray,this.resolvedProperty=l):Array.isArray(l)?(d=this.BindingType.EntireArray,this.resolvedProperty=l):this.propertyName=s;this.getValue=this.GetterByBindingType[d],this.setValue=this.SetterByBindingTypeAndVersioning[d][h]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};Gt.Composite=oc;Gt.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};Gt.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};Gt.prototype.GetterByBindingType=[Gt.prototype._getValue_direct,Gt.prototype._getValue_array,Gt.prototype._getValue_arrayElement,Gt.prototype._getValue_toArray];Gt.prototype.SetterByBindingTypeAndVersioning=[[Gt.prototype._setValue_direct,Gt.prototype._setValue_direct_setNeedsUpdate,Gt.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[Gt.prototype._setValue_array,Gt.prototype._setValue_array_setNeedsUpdate,Gt.prototype._setValue_array_setMatrixWorldNeedsUpdate],[Gt.prototype._setValue_arrayElement,Gt.prototype._setValue_arrayElement_setNeedsUpdate,Gt.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[Gt.prototype._setValue_fromArray,Gt.prototype._setValue_fromArray_setNeedsUpdate,Gt.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var sM=new Float32Array(1);var gu=new Ot,Cs=class{constructor(e,t,n=0,s=1/0){this.ray=new Di(e,t),this.near=n,this.far=s,this.camera=null,this.layers=new Nr,this.params={Mesh:{},Line:{threshold:1},LOD:{},Points:{threshold:1},Sprite:{}}}set(e,t){this.ray.set(e,t)}setFromCamera(e,t){t.isPerspectiveCamera?(this.ray.origin.setFromMatrixPosition(t.matrixWorld),this.ray.direction.set(e.x,e.y,.5).unproject(t).sub(this.ray.origin).normalize(),this.camera=t):t.isOrthographicCamera?(this.ray.origin.set(e.x,e.y,t.projectionMatrix.elements[14]).unproject(t),this.ray.direction.set(0,0,-1).transformDirection(t.matrixWorld),this.camera=t):it("Raycaster: Unsupported camera type: "+t.type)}setFromXRController(e){return gu.identity().extractRotation(e.matrixWorld),this.ray.origin.setFromMatrixPosition(e.matrixWorld),this.ray.direction.set(0,0,-1).applyMatrix4(gu),this}intersectObject(e,t=!0,n=[]){return lc(e,this,n,t),n.sort(_u),n}intersectObjects(e,t=!0,n=[]){for(let s=0,o=e.length;s<o;s++)lc(e[s],this,n,t);return n.sort(_u),n}};function _u(i,e){return i.distance-e.distance}function lc(i,e,t,n){let s=!0;if(i.layers.test(e.layers)&&i.raycast(e,t)===!1&&(s=!1),s===!0&&n===!0){let o=i.children;for(let l=0,h=o.length;l<h;l++)lc(o[l],e,t,!0)}}var Gr=class{constructor(e=1,t=0,n=0){this.radius=e,this.phi=t,this.theta=n}set(e,t,n){return this.radius=e,this.phi=t,this.theta=n,this}copy(e){return this.radius=e.radius,this.phi=e.phi,this.theta=e.theta,this}makeSafe(){return this.phi=_t(this.phi,1e-6,Math.PI-1e-6),this}setFromVector3(e){return this.setFromCartesianCoords(e.x,e.y,e.z)}setFromCartesianCoords(e,t,n){return this.radius=Math.sqrt(e*e+t*t+n*n),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(e,n),this.phi=Math.acos(_t(t/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}};var cc=class i{static{i.prototype.isMatrix2=!0}constructor(e,t,n,s){this.elements=[1,0,0,1],e!==void 0&&this.set(e,t,n,s)}identity(){return this.set(1,0,0,1),this}fromArray(e,t=0){for(let n=0;n<4;n++)this.elements[n]=e[n+t];return this}set(e,t,n,s){let o=this.elements;return o[0]=e,o[2]=t,o[1]=n,o[3]=s,this}};var vu=new j,La,tc,Rs=class extends on{constructor(e=new j(0,0,1),t=new j(0,0,0),n=1,s=16776960,o=n*.2,l=o*.2){super(),this.type="ArrowHelper",La===void 0&&(La=new Yt,La.setAttribute("position",new zt([0,0,0,0,1,0],3)),tc=new eo(.5,1,5,1),tc.translate(0,-.5,0)),this.position.copy(t),this.line=new vs(La,new kr({color:s,toneMapped:!1})),this.line.matrixAutoUpdate=!1,this.add(this.line),this.cone=new yn(tc,new Or({color:s,toneMapped:!1})),this.cone.matrixAutoUpdate=!1,this.add(this.cone),this.setDirection(e),this.setLength(n,o,l)}setDirection(e){if(e.y>.99999)this.quaternion.set(0,0,0,1);else if(e.y<-.99999)this.quaternion.set(1,0,0,0);else{vu.set(e.z,0,-e.x).normalize();let t=Math.acos(e.y);this.quaternion.setFromAxisAngle(vu,t)}}setLength(e,t=e*.2,n=t*.2){this.line.scale.set(1,Math.max(1e-4,e-t),1),this.line.updateMatrix(),this.cone.scale.set(n,t,n),this.cone.position.y=e,this.cone.updateMatrix()}setColor(e){this.line.material.color.set(e),this.cone.material.color.set(e)}copy(e){return super.copy(e,!1),this.line.copy(e.line),this.cone.copy(e.cone),this}dispose(){super.dispose(),this.line.geometry.dispose(),this.line.material.dispose(),this.cone.geometry.dispose(),this.cone.material.dispose()}},Ps=class extends Ka{constructor(e=1){let t=[0,0,0,e,0,0,0,0,0,0,e,0,0,0,0,0,0,e],n=[1,0,0,1,.6,0,0,1,0,.6,1,0,0,0,1,0,.6,1],s=new Yt;s.setAttribute("position",new zt(t,3)),s.setAttribute("color",new zt(n,3));let o=new kr({vertexColors:!0,toneMapped:!1});super(s,o),this.type="AxesHelper"}setColors(e,t,n){let s=new ht,o=this.geometry.attributes.color.array;return s.set(e),s.toArray(o,0),s.toArray(o,3),s.set(t),s.toArray(o,6),s.toArray(o,9),s.set(n),s.toArray(o,12),s.toArray(o,15),this.geometry.attributes.color.needsUpdate=!0,this}dispose(){super.dispose(),this.geometry.dispose(),this.material.dispose()}};var Is=class extends Zn{constructor(e,t=null){super(),this.object=e,this.domElement=t,this.enabled=!0,this.state=-1,this.keys={},this.mouseButtons={LEFT:null,MIDDLE:null,RIGHT:null},this.touches={ONE:null,TWO:null}}connect(e){this.domElement!==null&&this.disconnect(),this.domElement=e}disconnect(){}dispose(){}update(){}};function Bc(i,e,t,n){let s=q0(n);switch(t){case Cc:return i*e;case Pc:return i*e/s.components*s.byteLength;case wo:return i*e/s.components*s.byteLength;case Hi:return i*e*2/s.components*s.byteLength;case To:return i*e*2/s.components*s.byteLength;case Rc:return i*e*3/s.components*s.byteLength;case kn:return i*e*4/s.components*s.byteLength;case Ao:return i*e*4/s.components*s.byteLength;case Ns:case Us:return Math.floor((i+3)/4)*Math.floor((e+3)/4)*8;case Os:case Bs:return Math.floor((i+3)/4)*Math.floor((e+3)/4)*16;case Ro:case Io:return Math.max(i,16)*Math.max(e,8)/4;case Co:case Po:return Math.max(i,8)*Math.max(e,8)/2;case Do:case Lo:case No:case Uo:return Math.floor((i+3)/4)*Math.floor((e+3)/4)*8;case Fo:case ks:case Oo:return Math.floor((i+3)/4)*Math.floor((e+3)/4)*16;case Bo:return Math.floor((i+3)/4)*Math.floor((e+3)/4)*16;case ko:return Math.floor((i+4)/5)*Math.floor((e+3)/4)*16;case zo:return Math.floor((i+4)/5)*Math.floor((e+4)/5)*16;case Vo:return Math.floor((i+5)/6)*Math.floor((e+4)/5)*16;case Go:return Math.floor((i+5)/6)*Math.floor((e+5)/6)*16;case Ho:return Math.floor((i+7)/8)*Math.floor((e+4)/5)*16;case Wo:return Math.floor((i+7)/8)*Math.floor((e+5)/6)*16;case Xo:return Math.floor((i+7)/8)*Math.floor((e+7)/8)*16;case $o:return Math.floor((i+9)/10)*Math.floor((e+4)/5)*16;case jo:return Math.floor((i+9)/10)*Math.floor((e+5)/6)*16;case qo:return Math.floor((i+9)/10)*Math.floor((e+7)/8)*16;case Yo:return Math.floor((i+9)/10)*Math.floor((e+9)/10)*16;case Zo:return Math.floor((i+11)/12)*Math.floor((e+9)/10)*16;case Jo:return Math.floor((i+11)/12)*Math.floor((e+11)/12)*16;case Ko:case Qo:case el:return Math.ceil(i/4)*Math.ceil(e/4)*16;case tl:case nl:return Math.ceil(i/4)*Math.ceil(e/4)*8;case zs:case il:return Math.ceil(i/4)*Math.ceil(e/4)*16}throw new Error(`Unable to determine texture byte length for ${t} format.`)}function q0(i){switch(i){case En:case Ec:return{byteLength:1,components:1};case Xr:case wc:case ei:return{byteLength:2,components:1};case Mo:case Eo:return{byteLength:2,components:4};case Kn:case bo:case Qn:return{byteLength:4,components:1};case Tc:case Ac:return{byteLength:4,components:3}}throw new Error(`THREE.TextureUtils: Unknown texture type ${i}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:"186"}}));typeof window<"u"&&(window.__THREE__?et("WARNING: Multiple instances of Three.js being imported."):window.__THREE__="186");function Cd(){let i=null,e=!1,t=null,n=null;function s(o,l){n=i.requestAnimationFrame(s),t(o,l)}return{start:function(){e!==!0&&t!==null&&i!==null&&(n=i.requestAnimationFrame(s),e=!0)},stop:function(){i!==null&&i.cancelAnimationFrame(n),e=!1},setAnimationLoop:function(o){t=o},setContext:function(o){i=o}}}function Z0(i){let e=new WeakMap;function t(h,d){let f=h.array,g=h.usage,y=f.byteLength,m=i.createBuffer();i.bindBuffer(d,m),i.bufferData(d,f,g),h.onUploadCallback();let S;if(f instanceof Float32Array)S=i.FLOAT;else if(typeof Float16Array<"u"&&f instanceof Float16Array)S=i.HALF_FLOAT;else if(f instanceof Uint16Array)h.isFloat16BufferAttribute?S=i.HALF_FLOAT:S=i.UNSIGNED_SHORT;else if(f instanceof Int16Array)S=i.SHORT;else if(f instanceof Uint32Array)S=i.UNSIGNED_INT;else if(f instanceof Int32Array)S=i.INT;else if(f instanceof Int8Array)S=i.BYTE;else if(f instanceof Uint8Array)S=i.UNSIGNED_BYTE;else if(f instanceof Uint8ClampedArray)S=i.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+f);return{buffer:m,type:S,bytesPerElement:f.BYTES_PER_ELEMENT,version:h.version,size:y}}function n(h,d,f){let g=d.array,y=d.updateRanges;if(i.bindBuffer(f,h),y.length===0)i.bufferSubData(f,0,g);else{y.sort((S,T)=>S.start-T.start);let m=0;for(let S=1;S<y.length;S++){let T=y[m],P=y[S];P.start<=T.start+T.count+1?T.count=Math.max(T.count,P.start+P.count-T.start):(++m,y[m]=P)}y.length=m+1;for(let S=0,T=y.length;S<T;S++){let P=y[S];i.bufferSubData(f,P.start*g.BYTES_PER_ELEMENT,g,P.start,P.count)}d.clearUpdateRanges()}d.onUploadCallback()}function s(h){return h.isInterleavedBufferAttribute&&(h=h.data),e.get(h)}function o(h){h.isInterleavedBufferAttribute&&(h=h.data);let d=e.get(h);d&&(i.deleteBuffer(d.buffer),e.delete(h))}function l(h,d){if(h.isInterleavedBufferAttribute&&(h=h.data),h.isGLBufferAttribute){let g=e.get(h);(!g||g.version<h.version)&&e.set(h,{buffer:h.buffer,type:h.type,bytesPerElement:h.elementSize,version:h.version});return}let f=e.get(h);if(f===void 0)e.set(h,t(h,d));else if(f.version<h.version){if(f.size!==h.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");n(f.buffer,h,d),f.version=h.version}}return{get:s,remove:o,update:l}}var J0=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,K0=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,Q0=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,ev=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,tv=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,nv=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,iv=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,rv=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,sv=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec4 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 );
	}
#endif`,av=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,ov=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,lv=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,cv=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,hv=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,uv=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,dv=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,fv=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,pv=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,mv=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,gv=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#endif`,_v=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#endif`,vv=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec4 vColor;
#endif`,yv=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec4( 1.0 );
#endif
#ifdef USE_COLOR_ALPHA
	vColor *= color;
#elif defined( USE_COLOR )
	vColor.rgb *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.rgb *= instanceColor.rgb;
#endif
#ifdef USE_BATCHING_COLOR
	vColor *= getBatchingColor( getIndirectIndex( gl_DrawID ) );
#endif`,xv=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
#define inverseTransformDirection transformDirectionByInverseViewMatrix
vec3 transformNormalByInverseViewMatrix( in vec3 normal, in mat4 viewMatrix ) {
	return normalize( ( vec4( normal, 0.0 ) * viewMatrix ).xyz );
}
vec3 transformDirectionByInverseViewMatrix( in vec3 dir, in mat4 viewMatrix ) {
	return normalize( ( vec4( dir, 0.0 ) * viewMatrix ).xyz );
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,Sv=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,bv=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
#endif`,Mv=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Ev=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,wv=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,Tv=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Av="gl_FragColor = linearToOutputTexel( gl_FragColor );",Cv=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Rv=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * reflectVec );
		#ifdef ENVMAP_BLENDING_MULTIPLY
			outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_MIX )
			outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_ADD )
			outgoingLight += envColor.xyz * specularStrength * reflectivity;
		#endif
	#endif
#endif`,Pv=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
#endif`,Iv=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,Dv=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Lv=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = transformNormalByInverseViewMatrix( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,Fv=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Nv=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,Uv=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Ov=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,Bv=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,kv=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,zv=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,Vv=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,Gv=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_SUN_LIGHTS > 0
	struct SunLight {
		vec3 direction;
		vec3 color;
	};
	uniform SunLight sunLights[ NUM_SUN_LIGHTS ];
	void getSunLightInfo( const in SunLight sunLight, out IncidentLight light ) {
		light.color = sunLight.color;
		light.direction = sunLight.direction;
		light.visible = true;
	}
#endif
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif
#include <lightprobes_pars_fragment>`,Hv=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = transformNormalByInverseViewMatrix( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, pow4( roughness ) ) );
			reflectVec = transformDirectionByInverseViewMatrix( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_RETROREFLECTION
		vec3 getIBLRetroRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 retroVec = normalize( mix( viewDir, normal, pow4( roughness ) ) );
				retroVec = transformDirectionByInverseViewMatrix( retroVec, viewMatrix );
				vec4 envMapColor = textureCubeUV( envMap, envMapRotation * retroVec, roughness );
				return envMapColor.rgb * envMapIntensity;
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
		#ifdef USE_RETROREFLECTION
			vec3 getIBLAnisotropyRetroRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
				#ifdef ENVMAP_TYPE_CUBE_UV
					vec3 bentNormal = cross( bitangent, viewDir );
					bentNormal = normalize( cross( bentNormal, bitangent ) );
					bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
					return getIBLRetroRadiance( viewDir, bentNormal, roughness );
				#else
					return vec3( 0.0 );
				#endif
			}
		#endif
	#endif
#endif`,Wv=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,Xv=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,$v=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,jv=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,qv=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.diffuseContribution = diffuseColor.rgb * ( 1.0 - metalnessFactor );
material.metalness = metalnessFactor;
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor;
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = vec3( 0.04 );
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_RETROREFLECTION
	material.retroreflectivity = retroreflectivity;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.0001, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,Yv=`uniform sampler2D dfgLUT;
struct PhysicalMaterial {
	vec3 diffuseColor;
	vec3 diffuseContribution;
	vec3 specularColor;
	vec3 specularColorBlended;
	float roughness;
	float metalness;
	float specularF90;
	float dispersion;
	vec2 dfg;
	vec3 multiScatteringCompensation;
	#ifdef USE_RETROREFLECTION
		float retroreflectivity;
	#endif
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0Dielectric;
		vec3 iridescenceF0Metallic;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		return 0.5 / max( gv + gl, EPSILON );
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColorBlended;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transpose( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float rInv = 1.0 / ( roughness + 0.1 );
	float a = -1.9362 + 1.0678 * roughness + 0.4573 * r2 - 0.8469 * rInv;
	float b = -0.6014 + 0.5538 * roughness - 0.4670 * r2 - 0.1255 * rInv;
	float DG = exp( a * dotNV + b );
	return saturate( DG );
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec2 fab, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec2 fab, const in vec3 specularColor, const in float specularF90, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColorBlended * t2.x + ( material.specularF90 - material.specularColorBlended ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseContribution * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
		#ifdef USE_CLEARCOAT
			vec3 Ncc = geometryClearcoatNormal;
			vec2 uvClearcoat = LTC_Uv( Ncc, viewDir, material.clearcoatRoughness );
			vec4 t1Clearcoat = texture2D( ltc_1, uvClearcoat );
			vec4 t2Clearcoat = texture2D( ltc_2, uvClearcoat );
			mat3 mInvClearcoat = mat3(
				vec3( t1Clearcoat.x, 0, t1Clearcoat.y ),
				vec3(             0, 1,             0 ),
				vec3( t1Clearcoat.z, 0, t1Clearcoat.w )
			);
			vec3 fresnelClearcoat = material.clearcoatF0 * t2Clearcoat.x + ( material.clearcoatF90 - material.clearcoatF0 ) * t2Clearcoat.y;
			clearcoatSpecularDirect += lightColor * fresnelClearcoat * LTC_Evaluate( Ncc, viewDir, position, mInvClearcoat, rectCoords );
		#endif
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
 
 		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
 
 		float sheenAlbedoV = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
 		float sheenAlbedoL = IBLSheenBRDF( geometryNormal, directLight.direction, material.sheenRoughness );
 
 		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * max( sheenAlbedoV, sheenAlbedoL );
 
 		irradiance *= sheenEnergyComp;
 
 	#endif
	vec3 specularBRDF = BRDF_GGX( directLight.direction, geometryViewDir, geometryNormal, material );
	#ifdef USE_RETROREFLECTION
		vec3 retroViewDir = reflect( - geometryViewDir, geometryNormal );
		vec3 retroSpecularBRDF = BRDF_GGX( directLight.direction, retroViewDir, geometryNormal, material );
		specularBRDF = mix( specularBRDF, retroSpecularBRDF, saturate( material.retroreflectivity ) );
	#endif
	reflectedLight.directSpecular += irradiance * specularBRDF * material.multiScatteringCompensation;
	vec3 halfDir = normalize( directLight.direction + geometryViewDir );
	float dotVH = saturate( dot( geometryViewDir, halfDir ) );
	vec3 F = F_Schlick( material.specularColor, material.specularF90, dotVH );
	#ifdef USE_RETROREFLECTION
		vec3 retroHalfDir = normalize( directLight.direction + retroViewDir );
		float dotRetroVH = saturate( dot( retroViewDir, retroHalfDir ) );
		vec3 retroF = F_Schlick( material.specularColor, material.specularF90, dotRetroVH );
		F = mix( F, retroF, saturate( material.retroreflectivity ) );
	#endif
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution ) * ( 1.0 - F );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 singleScattering = vec3( 0.0 );
	vec3 multiScattering = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( material.dfg, material.specularColor, material.specularF90, material.iridescence, material.iridescenceF0Dielectric, singleScattering, multiScattering );
	#else
		computeMultiscattering( material.dfg, material.specularColor, material.specularF90, singleScattering, multiScattering );
	#endif
	vec3 diffuse = irradiance * BRDF_Lambert( material.diffuseContribution ) * ( 1.0 - singleScattering - multiScattering );
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		sheenSpecularIndirect += irradiance * material.sheenColor * sheenAlbedo * RECIPROCAL_PI;
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		diffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectDiffuse += diffuse;
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness ) * RECIPROCAL_PI;
 	#endif
	vec3 singleScatteringDielectric = vec3( 0.0 );
	vec3 multiScatteringDielectric = vec3( 0.0 );
	vec3 singleScatteringMetallic = vec3( 0.0 );
	vec3 multiScatteringMetallic = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( material.dfg, material.specularColor, material.specularF90, material.iridescence, material.iridescenceF0Dielectric, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscatteringIridescence( material.dfg, material.diffuseColor, material.specularF90, material.iridescence, material.iridescenceF0Metallic, singleScatteringMetallic, multiScatteringMetallic );
	#else
		computeMultiscattering( material.dfg, material.specularColor, material.specularF90, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscattering( material.dfg, material.diffuseColor, material.specularF90, singleScatteringMetallic, multiScatteringMetallic );
	#endif
	vec3 singleScattering = mix( singleScatteringDielectric, singleScatteringMetallic, material.metalness );
	vec3 multiScattering = mix( multiScatteringDielectric, multiScatteringMetallic, material.metalness );
	vec3 totalScatteringDielectric = singleScatteringDielectric + multiScatteringDielectric;
	vec3 diffuse = material.diffuseContribution * ( 1.0 - totalScatteringDielectric );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	vec3 indirectSpecular = radiance * singleScattering;
	indirectSpecular += multiScattering * cosineWeightedIrradiance;
	vec3 indirectDiffuse = diffuse * cosineWeightedIrradiance;
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		indirectSpecular *= sheenEnergyComp;
		indirectDiffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectSpecular += indirectSpecular;
	reflectedLight.indirectDiffuse += indirectDiffuse;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,Zv=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		vec3 iridescenceFresnelDielectric = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		vec3 iridescenceFresnelMetallic = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.diffuseColor );
		material.iridescenceFresnel = mix( iridescenceFresnelDielectric, iridescenceFresnelMetallic, material.metalness );
		material.iridescenceF0Dielectric = Schlick_to_F0( iridescenceFresnelDielectric, 1.0, dotNVi );
		material.iridescenceF0Metallic = Schlick_to_F0( iridescenceFresnelMetallic, 1.0, dotNVi );
	}
#endif
#ifdef STANDARD
	float dotNVms = saturate( dot( geometryNormal, geometryViewDir ) );
	material.dfg = texture2D( dfgLUT, vec2( material.roughness, dotNVms ) ).rg;
	#if ( NUM_SUN_LIGHTS > 0 || NUM_DIR_LIGHTS > 0 || NUM_POINT_LIGHTS > 0 || NUM_SPOT_LIGHTS > 0 )
		float EssMs = material.dfg.x + material.dfg.y;
		material.multiScatteringCompensation = 1.0 + material.specularColorBlended * ( 1.0 / EssMs - 1.0 );
	#endif
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS ) && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SUN_LIGHTS > 0 ) && defined( RE_Direct )
	SunLight sunLight;
	#if defined( USE_SHADOWMAP ) && NUM_SUN_LIGHT_SHADOWS > 0
	SunLightShadow sunLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SUN_LIGHTS; i ++ ) {
		sunLight = sunLights[ i ];
		getSunLightInfo( sunLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SUN_LIGHT_SHADOWS )
		sunLightShadow = sunLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getSunShadow( sunShadowMap[ i ], sunLightShadow, UNROLLED_LOOP_INDEX ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
	#ifdef USE_LIGHT_PROBES_GRID
		vec3 probeWorldPos = ( ( vec4( geometryPosition, 1.0 ) - viewMatrix[ 3 ] ) * viewMatrix ).xyz;
		vec3 probeWorldNormal = transformNormalByInverseViewMatrix( geometryNormal, viewMatrix );
		irradiance += getLightProbeGridIrradiance( probeWorldPos, probeWorldNormal );
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,Jv=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( ENVMAP_TYPE_CUBE_UV )
		#if defined( STANDARD ) || defined( LAMBERT ) || defined( PHONG )
			iblIrradiance += getIBLIrradiance( geometryNormal );
		#endif
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		vec3 iblRadiance = getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		vec3 iblRadiance = getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_RETROREFLECTION
		#ifdef USE_ANISOTROPY
			vec3 retroIBLRadiance = getIBLAnisotropyRetroRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
		#else
			vec3 retroIBLRadiance = getIBLRetroRadiance( geometryViewDir, geometryNormal, material.roughness );
		#endif
		iblRadiance = mix( iblRadiance, retroIBLRadiance, saturate( material.retroreflectivity ) );
	#endif
	radiance += iblRadiance;
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,Kv=`#if defined( RE_IndirectDiffuse )
	#if defined( LAMBERT ) || defined( PHONG )
		irradiance += iblIrradiance;
	#endif
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,Qv=`#ifdef USE_LIGHT_PROBES_GRID
uniform highp sampler3D probesSH;
uniform vec3 probesMin;
uniform vec3 probesMax;
uniform vec3 probesResolution;
vec3 getLightProbeGridIrradiance( vec3 worldPos, vec3 worldNormal ) {
	vec3 res = probesResolution;
	vec3 gridRange = probesMax - probesMin;
	vec3 resMinusOne = res - 1.0;
	vec3 probeSpacing = gridRange / resMinusOne;
	vec3 samplePos = worldPos + worldNormal * probeSpacing * 0.5;
	vec3 uvw = clamp( ( samplePos - probesMin ) / gridRange, 0.0, 1.0 );
	uvw = uvw * resMinusOne / res + 0.5 / res;
	float nz          = res.z;
	float paddedSlices = nz + 2.0;
	float atlasDepth  = 7.0 * paddedSlices;
	float uvZBase     = uvw.z * nz + 1.0;
	vec4 s0 = texture( probesSH, vec3( uvw.xy, ( uvZBase                       ) / atlasDepth ) );
	vec4 s1 = texture( probesSH, vec3( uvw.xy, ( uvZBase +       paddedSlices   ) / atlasDepth ) );
	vec4 s2 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 2.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s3 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 3.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s4 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 4.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s5 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 5.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s6 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 6.0 * paddedSlices   ) / atlasDepth ) );
	vec3 c0 = s0.xyz;
	vec3 c1 = vec3( s0.w, s1.xy );
	vec3 c2 = vec3( s1.zw, s2.x );
	vec3 c3 = s2.yzw;
	vec3 c4 = s3.xyz;
	vec3 c5 = vec3( s3.w, s4.xy );
	vec3 c6 = vec3( s4.zw, s5.x );
	vec3 c7 = s5.yzw;
	vec3 c8 = s6.xyz;
	float x = worldNormal.x, y = worldNormal.y, z = worldNormal.z;
	vec3 result = c0 * 0.886227;
	result += c1 * 2.0 * 0.511664 * y;
	result += c2 * 2.0 * 0.511664 * z;
	result += c3 * 2.0 * 0.511664 * x;
	result += c4 * 2.0 * 0.429043 * x * y;
	result += c5 * 2.0 * 0.429043 * y * z;
	result += c6 * ( 0.743125 * z * z - 0.247708 );
	result += c7 * 2.0 * 0.429043 * x * z;
	result += c8 * 0.429043 * ( x * x - y * y );
	return max( result, vec3( 0.0 ) );
}
#endif`,ey=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,ty=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,ny=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,iy=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,ry=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,sy=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,ay=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,oy=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,ly=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,cy=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,hy=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,uy=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,dy=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,fy=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,py=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,my=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#ifdef DOUBLE_SIDED
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#ifdef DOUBLE_SIDED
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,gy=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#if defined( USE_PACKED_NORMALMAP )
		mapN = vec3( mapN.xy, sqrt( saturate( 1.0 - dot( mapN.xy, mapN.xy ) ) ) );
	#endif
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,_y=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,vy=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,yy=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
		#ifdef FLIP_SIDED
			vBitangent = - vBitangent;
		#endif
	#endif
#endif`,xy=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,Sy=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,by=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,My=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,Ey=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,wy=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,Ty=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	#ifdef USE_REVERSED_DEPTH_BUFFER
	
		return depth * ( far - near ) - far;
	#else
		return depth * ( near - far ) - near;
	#endif
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	
	#ifdef USE_REVERSED_DEPTH_BUFFER
		return ( near * far ) / ( ( near - far ) * depth - near );
	#else
		return ( near * far ) / ( ( far - near ) * depth - far );
	#endif
}`,Ay=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,Cy=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,Ry=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,Py=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,Iy=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,Dy=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Ly=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
		#define SUN_LIGHT_CASCADES 2
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow sunShadowMap[ NUM_SUN_LIGHT_SHADOWS ];
		#else
			uniform sampler2D sunShadowMap[ NUM_SUN_LIGHT_SHADOWS ];
		#endif
		uniform mat4 sunShadowMatrix[ NUM_SUN_LIGHT_SHADOWS * SUN_LIGHT_CASCADES ];
		uniform vec4 sunShadowCascade[ NUM_SUN_LIGHT_SHADOWS * SUN_LIGHT_CASCADES ];
		varying vec4 vSunShadowWorldPosition;
		varying vec3 vSunShadowWorldNormal;
		struct SunLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SunLightShadow sunLightShadows[ NUM_SUN_LIGHT_SHADOWS ];
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#else
			uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#endif
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#else
			uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#endif
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform samplerCubeShadow pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#elif defined( SHADOWMAP_TYPE_BASIC )
			uniform samplerCube pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#endif
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float interleavedGradientNoise( vec2 position ) {
			return fract( 52.9829189 * fract( dot( position, vec2( 0.06711056, 0.00583715 ) ) ) );
		}
		vec2 vogelDiskSample( int sampleIndex, int samplesCount, float phi ) {
			const float goldenAngle = 2.399963229728653;
			float r = sqrt( ( float( sampleIndex ) + 0.5 ) / float( samplesCount ) );
			float theta = float( sampleIndex ) * goldenAngle + phi;
			return vec2( cos( theta ), sin( theta ) ) * r;
		}
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float getShadow( sampler2DShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
				float radius = shadowRadius * texelSize.x;
				float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
				shadow = (
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 0, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 1, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 2, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 3, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 4, 5, phi ) * radius, shadowCoord.z ) )
				) * 0.2;
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#elif defined( SHADOWMAP_TYPE_VSM )
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 distribution = texture2D( shadowMap, shadowCoord.xy ).rg;
				float mean = distribution.x;
				float variance = distribution.y * distribution.y;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					float hard_shadow = step( mean, shadowCoord.z );
				#else
					float hard_shadow = step( shadowCoord.z, mean );
				#endif
				
				if ( hard_shadow == 1.0 ) {
					shadow = 1.0;
				} else {
					variance = max( variance, 0.0000001 );
					float d = shadowCoord.z - mean;
					float p_max = variance / ( variance + d * d );
					p_max = clamp( ( p_max - 0.3 ) / 0.65, 0.0, 1.0 );
					shadow = max( hard_shadow, p_max );
				}
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#else
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				float depth = texture2D( shadowMap, shadowCoord.xy ).r;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					shadow = step( depth, shadowCoord.z );
				#else
					shadow = step( shadowCoord.z, depth );
				#endif
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#endif
	#if NUM_SUN_LIGHT_SHADOWS > 0
		float getSunShadow(
			#if defined( SHADOWMAP_TYPE_PCF )
				sampler2DShadow shadowMap,
			#else
				sampler2D shadowMap,
			#endif
			SunLightShadow sunLightShadow,
			int shadowIndex
		) {
			vec4 shadowWorldPosition = vec4( vSunShadowWorldPosition.xyz + vSunShadowWorldNormal * sunLightShadow.shadowNormalBias, 1.0 );
			float viewDepth = vSunShadowWorldPosition.w;
			int cascadeOffset = shadowIndex * SUN_LIGHT_CASCADES;
			float shadow = 1.0;
			for ( int i = SUN_LIGHT_CASCADES - 1; i >= 0; i -- ) {
				vec4 cascade = sunShadowCascade[ cascadeOffset + i ];
				if ( viewDepth >= cascade.x && viewDepth < cascade.y ) {
					float cascadeShadow = getShadow(
						shadowMap,
						sunLightShadow.shadowMapSize,
						sunLightShadow.shadowIntensity,
						sunLightShadow.shadowBias,
						sunLightShadow.shadowRadius,
						sunShadowMatrix[ cascadeOffset + i ] * shadowWorldPosition
					);
					shadow = mix( cascadeShadow, shadow, smoothstep( cascade.z, cascade.y, viewDepth ) );
				}
			}
			return shadow;
		}
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	#if defined( SHADOWMAP_TYPE_PCF )
	float getPointShadow( samplerCubeShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 bd3D = normalize( lightToPosition );
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			#ifdef USE_REVERSED_DEPTH_BUFFER
				float dp = ( shadowCameraNear * ( shadowCameraFar - viewSpaceZ ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp -= shadowBias;
			#else
				float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp += shadowBias;
			#endif
			float texelSize = shadowRadius / shadowMapSize.x;
			vec3 absDir = abs( bd3D );
			vec3 tangent = absDir.x > absDir.z ? vec3( 0.0, 1.0, 0.0 ) : vec3( 1.0, 0.0, 0.0 );
			tangent = normalize( cross( bd3D, tangent ) );
			vec3 bitangent = cross( bd3D, tangent );
			float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
			vec2 sample0 = vogelDiskSample( 0, 5, phi );
			vec2 sample1 = vogelDiskSample( 1, 5, phi );
			vec2 sample2 = vogelDiskSample( 2, 5, phi );
			vec2 sample3 = vogelDiskSample( 3, 5, phi );
			vec2 sample4 = vogelDiskSample( 4, 5, phi );
			shadow = (
				texture( shadowMap, vec4( bd3D + ( tangent * sample0.x + bitangent * sample0.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample1.x + bitangent * sample1.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample2.x + bitangent * sample2.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample3.x + bitangent * sample3.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample4.x + bitangent * sample4.y ) * texelSize, dp ) )
			) * 0.2;
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#elif defined( SHADOWMAP_TYPE_BASIC )
	float getPointShadow( samplerCube shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			float depth = textureCube( shadowMap, bd3D ).r;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				depth = 1.0 - depth;
			#endif
			shadow = step( dp, depth );
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#endif
	#endif
#endif`,Fy=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
		varying vec4 vSunShadowWorldPosition;
		varying vec3 vSunShadowWorldNormal;
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,Ny=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_SUN_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	#ifdef HAS_NORMAL
		vec3 shadowWorldNormal = transformNormalByInverseViewMatrix( transformedNormal, viewMatrix );
	#else
		vec3 shadowWorldNormal = vec3( 0.0 );
	#endif
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_SUN_LIGHT_SHADOWS > 0
		vSunShadowWorldPosition = vec4( worldPosition.xyz, - mvPosition.z );
		vSunShadowWorldNormal = shadowWorldNormal;
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,Uy=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_SUN_LIGHT_SHADOWS > 0
	SunLightShadow sunLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SUN_LIGHT_SHADOWS; i ++ ) {
		sunLight = sunLightShadows[ i ];
		shadow *= receiveShadow ? getSunShadow( sunShadowMap[ i ], sunLight, UNROLLED_LOOP_INDEX ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0 && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,Oy=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,By=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,ky=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,zy=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,Vy=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,Gy=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,Hy=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,Wy=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,Xy=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = transformNormalByInverseViewMatrix( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseContribution, material.specularColorBlended, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,$y=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,jy=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,qy=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,Yy=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,Zy=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,Jy=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,Ky=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,Qy=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,ex=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vWorldDirection );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,tx=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,nx=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,ix=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,rx=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSED_DEPTH_BUFFER
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,sx=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,ax=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = vec4( dist, 0.0, 0.0, 1.0 );
}`,ox=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,lx=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,cx=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,hx=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,ux=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,dx=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,fx=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,px=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,mx=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,gx=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,_x=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,vx=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( normalize( normal ) * 0.5 + 0.5, diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,yx=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,xx=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Sx=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,bx=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_RETROREFLECTION
	uniform float retroreflectivity;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
 
		outgoingLight = outgoingLight + sheenSpecularDirect + sheenSpecularIndirect;
 
 	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Mx=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Ex=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,wx=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,Tx=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Ax=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,Cx=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,Rx=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,Px=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,pt={alphahash_fragment:J0,alphahash_pars_fragment:K0,alphamap_fragment:Q0,alphamap_pars_fragment:ev,alphatest_fragment:tv,alphatest_pars_fragment:nv,aomap_fragment:iv,aomap_pars_fragment:rv,batching_pars_vertex:sv,batching_vertex:av,begin_vertex:ov,beginnormal_vertex:lv,bsdfs:cv,iridescence_fragment:hv,bumpmap_pars_fragment:uv,clipping_planes_fragment:dv,clipping_planes_pars_fragment:fv,clipping_planes_pars_vertex:pv,clipping_planes_vertex:mv,color_fragment:gv,color_pars_fragment:_v,color_pars_vertex:vv,color_vertex:yv,common:xv,cube_uv_reflection_fragment:Sv,defaultnormal_vertex:bv,displacementmap_pars_vertex:Mv,displacementmap_vertex:Ev,emissivemap_fragment:wv,emissivemap_pars_fragment:Tv,colorspace_fragment:Av,colorspace_pars_fragment:Cv,envmap_fragment:Rv,envmap_common_pars_fragment:Pv,envmap_pars_fragment:Iv,envmap_pars_vertex:Dv,envmap_physical_pars_fragment:Hv,envmap_vertex:Lv,fog_vertex:Fv,fog_pars_vertex:Nv,fog_fragment:Uv,fog_pars_fragment:Ov,gradientmap_pars_fragment:Bv,lightmap_pars_fragment:kv,lights_lambert_fragment:zv,lights_lambert_pars_fragment:Vv,lights_pars_begin:Gv,lights_toon_fragment:Wv,lights_toon_pars_fragment:Xv,lights_phong_fragment:$v,lights_phong_pars_fragment:jv,lights_physical_fragment:qv,lights_physical_pars_fragment:Yv,lights_fragment_begin:Zv,lights_fragment_maps:Jv,lights_fragment_end:Kv,lightprobes_pars_fragment:Qv,logdepthbuf_fragment:ey,logdepthbuf_pars_fragment:ty,logdepthbuf_pars_vertex:ny,logdepthbuf_vertex:iy,map_fragment:ry,map_pars_fragment:sy,map_particle_fragment:ay,map_particle_pars_fragment:oy,metalnessmap_fragment:ly,metalnessmap_pars_fragment:cy,morphinstance_vertex:hy,morphcolor_vertex:uy,morphnormal_vertex:dy,morphtarget_pars_vertex:fy,morphtarget_vertex:py,normal_fragment_begin:my,normal_fragment_maps:gy,normal_pars_fragment:_y,normal_pars_vertex:vy,normal_vertex:yy,normalmap_pars_fragment:xy,clearcoat_normal_fragment_begin:Sy,clearcoat_normal_fragment_maps:by,clearcoat_pars_fragment:My,iridescence_pars_fragment:Ey,opaque_fragment:wy,packing:Ty,premultiplied_alpha_fragment:Ay,project_vertex:Cy,dithering_fragment:Ry,dithering_pars_fragment:Py,roughnessmap_fragment:Iy,roughnessmap_pars_fragment:Dy,shadowmap_pars_fragment:Ly,shadowmap_pars_vertex:Fy,shadowmap_vertex:Ny,shadowmask_pars_fragment:Uy,skinbase_vertex:Oy,skinning_pars_vertex:By,skinning_vertex:ky,skinnormal_vertex:zy,specularmap_fragment:Vy,specularmap_pars_fragment:Gy,tonemapping_fragment:Hy,tonemapping_pars_fragment:Wy,transmission_fragment:Xy,transmission_pars_fragment:$y,uv_pars_fragment:jy,uv_pars_vertex:qy,uv_vertex:Yy,worldpos_vertex:Zy,background_vert:Jy,background_frag:Ky,backgroundCube_vert:Qy,backgroundCube_frag:ex,cube_vert:tx,cube_frag:nx,depth_vert:ix,depth_frag:rx,distance_vert:sx,distance_frag:ax,equirect_vert:ox,equirect_frag:lx,linedashed_vert:cx,linedashed_frag:hx,meshbasic_vert:ux,meshbasic_frag:dx,meshlambert_vert:fx,meshlambert_frag:px,meshmatcap_vert:mx,meshmatcap_frag:gx,meshnormal_vert:_x,meshnormal_frag:vx,meshphong_vert:yx,meshphong_frag:xx,meshphysical_vert:Sx,meshphysical_frag:bx,meshtoon_vert:Mx,meshtoon_frag:Ex,points_vert:wx,points_frag:Tx,shadow_vert:Ax,shadow_frag:Cx,sprite_vert:Rx,sprite_frag:Px},Fe={common:{diffuse:{value:new ht(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new at},alphaMap:{value:null},alphaMapTransform:{value:new at},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new at}},envmap:{envMap:{value:null},envMapRotation:{value:new at},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98},dfgLUT:{value:null}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new at}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new at}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new at},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new at},normalScale:{value:new nt(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new at},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new at}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new at}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new at}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ht(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},sunLights:{value:[],properties:{direction:{},color:{}}},sunLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},sunShadowMatrix:{value:[]},sunShadowCascade:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null},probesSH:{value:null},probesMin:{value:new j},probesMax:{value:new j},probesResolution:{value:new j}},points:{diffuse:{value:new ht(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new at},alphaTest:{value:0},uvTransform:{value:new at}},sprite:{diffuse:{value:new ht(16777215)},opacity:{value:1},center:{value:new nt(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new at},alphaMap:{value:null},alphaMapTransform:{value:new at},alphaTest:{value:0}}},di={basic:{uniforms:pn([Fe.common,Fe.specularmap,Fe.envmap,Fe.aomap,Fe.lightmap,Fe.fog]),vertexShader:pt.meshbasic_vert,fragmentShader:pt.meshbasic_frag},lambert:{uniforms:pn([Fe.common,Fe.specularmap,Fe.envmap,Fe.aomap,Fe.lightmap,Fe.emissivemap,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,Fe.fog,Fe.lights,{emissive:{value:new ht(0)},envMapIntensity:{value:1}}]),vertexShader:pt.meshlambert_vert,fragmentShader:pt.meshlambert_frag},phong:{uniforms:pn([Fe.common,Fe.specularmap,Fe.envmap,Fe.aomap,Fe.lightmap,Fe.emissivemap,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,Fe.fog,Fe.lights,{emissive:{value:new ht(0)},specular:{value:new ht(1118481)},shininess:{value:30},envMapIntensity:{value:1}}]),vertexShader:pt.meshphong_vert,fragmentShader:pt.meshphong_frag},standard:{uniforms:pn([Fe.common,Fe.envmap,Fe.aomap,Fe.lightmap,Fe.emissivemap,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,Fe.roughnessmap,Fe.metalnessmap,Fe.fog,Fe.lights,{emissive:{value:new ht(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:pt.meshphysical_vert,fragmentShader:pt.meshphysical_frag},toon:{uniforms:pn([Fe.common,Fe.aomap,Fe.lightmap,Fe.emissivemap,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,Fe.gradientmap,Fe.fog,Fe.lights,{emissive:{value:new ht(0)}}]),vertexShader:pt.meshtoon_vert,fragmentShader:pt.meshtoon_frag},matcap:{uniforms:pn([Fe.common,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,Fe.fog,{matcap:{value:null}}]),vertexShader:pt.meshmatcap_vert,fragmentShader:pt.meshmatcap_frag},points:{uniforms:pn([Fe.points,Fe.fog]),vertexShader:pt.points_vert,fragmentShader:pt.points_frag},dashed:{uniforms:pn([Fe.common,Fe.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:pt.linedashed_vert,fragmentShader:pt.linedashed_frag},depth:{uniforms:pn([Fe.common,Fe.displacementmap]),vertexShader:pt.depth_vert,fragmentShader:pt.depth_frag},normal:{uniforms:pn([Fe.common,Fe.bumpmap,Fe.normalmap,Fe.displacementmap,{opacity:{value:1}}]),vertexShader:pt.meshnormal_vert,fragmentShader:pt.meshnormal_frag},sprite:{uniforms:pn([Fe.sprite,Fe.fog]),vertexShader:pt.sprite_vert,fragmentShader:pt.sprite_frag},background:{uniforms:{uvTransform:{value:new at},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:pt.background_vert,fragmentShader:pt.background_frag},backgroundCube:{uniforms:{envMap:{value:null},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new at}},vertexShader:pt.backgroundCube_vert,fragmentShader:pt.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:pt.cube_vert,fragmentShader:pt.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:pt.equirect_vert,fragmentShader:pt.equirect_frag},distance:{uniforms:pn([Fe.common,Fe.displacementmap,{referencePosition:{value:new j},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:pt.distance_vert,fragmentShader:pt.distance_frag},shadow:{uniforms:pn([Fe.lights,Fe.fog,{color:{value:new ht(0)},opacity:{value:1}}]),vertexShader:pt.shadow_vert,fragmentShader:pt.shadow_frag}};di.physical={uniforms:pn([di.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new at},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new at},clearcoatNormalScale:{value:new nt(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new at},dispersion:{value:0},retroreflectivity:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new at},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new at},sheen:{value:0},sheenColor:{value:new ht(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new at},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new at},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new at},transmissionSamplerSize:{value:new nt},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new at},attenuationDistance:{value:0},attenuationColor:{value:new ht(0)},specularColor:{value:new ht(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new at},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new at},anisotropyVector:{value:new nt},anisotropyMap:{value:null},anisotropyMapTransform:{value:new at}}]),vertexShader:pt.meshphysical_vert,fragmentShader:pt.meshphysical_frag};var ol={r:0,b:0,g:0},Ix=new Ot,Rd=new at;Rd.set(-1,0,0,0,1,0,0,0,1);function Dx(i,e,t,n,s,o){let l=new ht(0),h=s===!0?0:1,d,f,g=null,y=0,m=null;function S(U){let z=U.isScene===!0?U.background:null;if(z&&z.isTexture){let R=U.backgroundBlurriness>0;z=e.get(z,R)}return z}function T(U){let z=!1,R=S(U);R===null?b(l,h):R&&R.isColor&&(b(R,1),z=!0);let I=i.xr.getEnvironmentBlendMode();I==="additive"?t.buffers.color.setClear(0,0,0,1,o):I==="alpha-blend"&&t.buffers.color.setClear(0,0,0,0,o),(i.autoClear||z)&&(t.buffers.depth.setTest(!0),t.buffers.depth.setMask(!0),t.buffers.color.setMask(!0),i.clear(i.autoClearColor,i.autoClearDepth,i.autoClearStencil))}function P(U,z){let R=S(z);R&&(R.isCubeTexture||R.mapping===Ls)?(f===void 0&&(f=new yn(new Fi(1,1,1),new Dn({name:"BackgroundCubeMaterial",uniforms:lr(di.backgroundCube.uniforms),vertexShader:di.backgroundCube.vertexShader,fragmentShader:di.backgroundCube.fragmentShader,side:xn,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),f.geometry.deleteAttribute("normal"),f.geometry.deleteAttribute("uv"),f.onBeforeRender=function(I,L,B){this.matrixWorld.copyPosition(B.matrixWorld)},Object.defineProperty(f.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),n.update(f)),f.material.uniforms.envMap.value=R,f.material.uniforms.backgroundBlurriness.value=z.backgroundBlurriness,f.material.uniforms.backgroundIntensity.value=z.backgroundIntensity,f.material.uniforms.backgroundRotation.value.setFromMatrix4(Ix.makeRotationFromEuler(z.backgroundRotation)).transpose(),R.isCubeTexture&&R.isRenderTargetTexture===!1&&f.material.uniforms.backgroundRotation.value.premultiply(Rd),f.material.toneMapped=xt.getTransfer(R.colorSpace)!==It,(g!==R||y!==R.version||m!==i.toneMapping)&&(f.material.needsUpdate=!0,g=R,y=R.version,m=i.toneMapping),f.layers.enableAll(),U.unshift(f,f.geometry,f.material,0,0,null)):R&&R.isTexture&&(d===void 0&&(d=new yn(new sr(2,2),new Dn({name:"BackgroundMaterial",uniforms:lr(di.background.uniforms),vertexShader:di.background.vertexShader,fragmentShader:di.background.fragmentShader,side:li,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),d.geometry.deleteAttribute("normal"),Object.defineProperty(d.material,"map",{get:function(){return this.uniforms.t2D.value}}),n.update(d)),d.material.uniforms.t2D.value=R,d.material.uniforms.backgroundIntensity.value=z.backgroundIntensity,d.material.toneMapped=xt.getTransfer(R.colorSpace)!==It,R.matrixAutoUpdate===!0&&R.updateMatrix(),d.material.uniforms.uvTransform.value.copy(R.matrix),(g!==R||y!==R.version||m!==i.toneMapping)&&(d.material.needsUpdate=!0,g=R,y=R.version,m=i.toneMapping),d.layers.enableAll(),U.unshift(d,d.geometry,d.material,0,0,null))}function b(U,z){U.getRGB(ol,Nc(i)),t.buffers.color.setClear(ol.r,ol.g,ol.b,z,o)}function _(){f!==void 0&&(f.geometry.dispose(),f.material.dispose(),f=void 0),d!==void 0&&(d.geometry.dispose(),d.material.dispose(),d=void 0)}return{getClearColor:function(){return l},setClearColor:function(U,z=1){l.set(U),h=z,b(l,h)},getClearAlpha:function(){return h},setClearAlpha:function(U){h=U,b(l,h)},render:T,addToRenderList:P,dispose:_}}function Lx(i,e){let t=i.getParameter(i.MAX_VERTEX_ATTRIBS),n={},s=m(null),o=s,l=!1;function h(q,Y,J,H,te){let k=!1,se=y(q,H,J,Y);o!==se&&(o=se,f(o.object)),k=S(q,H,J,te),k&&T(q,H,J,te),te!==null&&e.update(te,i.ELEMENT_ARRAY_BUFFER),(k||l)&&(l=!1,R(q,Y,J,H),te!==null&&i.bindBuffer(i.ELEMENT_ARRAY_BUFFER,e.get(te).buffer))}function d(){return i.createVertexArray()}function f(q){return i.bindVertexArray(q)}function g(q){return i.deleteVertexArray(q)}function y(q,Y,J,H){let te=H.wireframe===!0,k=n[Y.id];k===void 0&&(k={},n[Y.id]=k);let se=q.isInstancedMesh===!0?q.id:0,_e=k[se];_e===void 0&&(_e={},k[se]=_e);let ae=_e[J.id];ae===void 0&&(ae={},_e[J.id]=ae);let V=ae[te];return V===void 0&&(V=m(d()),ae[te]=V),V}function m(q){let Y=[],J=[],H=[];for(let te=0;te<t;te++)Y[te]=0,J[te]=0,H[te]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:Y,enabledAttributes:J,attributeDivisors:H,object:q,attributes:{},index:null}}function S(q,Y,J,H){let te=o.attributes,k=Y.attributes,se=0,_e=J.getAttributes();for(let ae in _e)if(_e[ae].location>=0){let ge=te[ae],Ye=k[ae];if(Ye===void 0&&(ae==="instanceMatrix"&&q.instanceMatrix&&(Ye=q.instanceMatrix),ae==="instanceColor"&&q.instanceColor&&(Ye=q.instanceColor)),ge===void 0||ge.attribute!==Ye||Ye&&ge.data!==Ye.data)return!0;se++}return o.attributesNum!==se||o.index!==H}function T(q,Y,J,H){let te={},k=Y.attributes,se=0,_e=J.getAttributes();for(let ae in _e)if(_e[ae].location>=0){let ge=k[ae];ge===void 0&&(ae==="instanceMatrix"&&q.instanceMatrix&&(ge=q.instanceMatrix),ae==="instanceColor"&&q.instanceColor&&(ge=q.instanceColor));let Ye={};Ye.attribute=ge,ge&&ge.data&&(Ye.data=ge.data),te[ae]=Ye,se++}o.attributes=te,o.attributesNum=se,o.index=H}function P(){let q=o.newAttributes;for(let Y=0,J=q.length;Y<J;Y++)q[Y]=0}function b(q){_(q,0)}function _(q,Y){let J=o.newAttributes,H=o.enabledAttributes,te=o.attributeDivisors;J[q]=1,H[q]===0&&(i.enableVertexAttribArray(q),H[q]=1),te[q]!==Y&&(i.vertexAttribDivisor(q,Y),te[q]=Y)}function U(){let q=o.newAttributes,Y=o.enabledAttributes;for(let J=0,H=Y.length;J<H;J++)Y[J]!==q[J]&&(i.disableVertexAttribArray(J),Y[J]=0)}function z(q,Y,J,H,te,k,se){se===!0?i.vertexAttribIPointer(q,Y,J,te,k):i.vertexAttribPointer(q,Y,J,H,te,k)}function R(q,Y,J,H){P();let te=H.attributes,k=J.getAttributes(),se=Y.defaultAttributeValues;for(let _e in k){let ae=k[_e];if(ae.location>=0){let V=te[_e];if(V===void 0&&(_e==="instanceMatrix"&&q.instanceMatrix&&(V=q.instanceMatrix),_e==="instanceColor"&&q.instanceColor&&(V=q.instanceColor)),V!==void 0){let ge=V.normalized,Ye=V.itemSize,$e=e.get(V);if($e===void 0)continue;let Ut=$e.buffer,mt=$e.type,Ke=$e.bytesPerElement,le=mt===i.INT||mt===i.UNSIGNED_INT||V.gpuType===bo;if(V.isInterleavedBufferAttribute){let fe=V.data,ke=fe.stride,st=V.offset;if(fe.isInstancedInterleavedBuffer){for(let Be=0;Be<ae.locationSize;Be++)_(ae.location+Be,fe.meshPerAttribute);q.isInstancedMesh!==!0&&H._maxInstanceCount===void 0&&(H._maxInstanceCount=fe.meshPerAttribute*fe.count)}else for(let Be=0;Be<ae.locationSize;Be++)b(ae.location+Be);i.bindBuffer(i.ARRAY_BUFFER,Ut);for(let Be=0;Be<ae.locationSize;Be++)z(ae.location+Be,Ye/ae.locationSize,mt,ge,ke*Ke,(st+Ye/ae.locationSize*Be)*Ke,le)}else{if(V.isInstancedBufferAttribute){for(let fe=0;fe<ae.locationSize;fe++)_(ae.location+fe,V.meshPerAttribute);q.isInstancedMesh!==!0&&H._maxInstanceCount===void 0&&(H._maxInstanceCount=V.meshPerAttribute*V.count)}else for(let fe=0;fe<ae.locationSize;fe++)b(ae.location+fe);i.bindBuffer(i.ARRAY_BUFFER,Ut);for(let fe=0;fe<ae.locationSize;fe++)z(ae.location+fe,Ye/ae.locationSize,mt,ge,Ye*Ke,Ye/ae.locationSize*fe*Ke,le)}}else if(se!==void 0){let ge=se[_e];if(ge!==void 0)switch(ge.length){case 2:i.vertexAttrib2fv(ae.location,ge);break;case 3:i.vertexAttrib3fv(ae.location,ge);break;case 4:i.vertexAttrib4fv(ae.location,ge);break;default:i.vertexAttrib1fv(ae.location,ge)}}}}U()}function I(){D();for(let q in n){let Y=n[q];for(let J in Y){let H=Y[J];for(let te in H){let k=H[te];for(let se in k)g(k[se].object),delete k[se];delete H[te]}}delete n[q]}}function L(q){if(n[q.id]===void 0)return;let Y=n[q.id];for(let J in Y){let H=Y[J];for(let te in H){let k=H[te];for(let se in k)g(k[se].object),delete k[se];delete H[te]}}delete n[q.id]}function B(q){for(let Y in n){let J=n[Y];for(let H in J){let te=J[H];if(te[q.id]===void 0)continue;let k=te[q.id];for(let se in k)g(k[se].object),delete k[se];delete te[q.id]}}}function w(q){for(let Y in n){let J=n[Y],H=q.isInstancedMesh===!0?q.id:0,te=J[H];if(te!==void 0){for(let k in te){let se=te[k];for(let _e in se)g(se[_e].object),delete se[_e];delete te[k]}delete J[H],Object.keys(J).length===0&&delete n[Y]}}}function D(){O(),l=!0,o!==s&&(o=s,f(o.object))}function O(){s.geometry=null,s.program=null,s.wireframe=!1}return{setup:h,reset:D,resetDefaultState:O,dispose:I,releaseStatesOfGeometry:L,releaseStatesOfObject:w,releaseStatesOfProgram:B,initAttributes:P,enableAttribute:b,disableUnusedAttributes:U}}function Fx(i,e,t){let n;function s(d){n=d}function o(d,f){i.drawArrays(n,d,f),t.update(f,n,1)}function l(d,f,g){g!==0&&(i.drawArraysInstanced(n,d,f,g),t.update(f,n,g))}function h(d,f,g){if(g===0)return;e.get("WEBGL_multi_draw").multiDrawArraysWEBGL(n,d,0,f,0,g);let m=0;for(let S=0;S<g;S++)m+=f[S];t.update(m,n,1)}this.setMode=s,this.render=o,this.renderInstances=l,this.renderMultiDraw=h}function Nx(i,e,t,n){let s;function o(){if(s!==void 0)return s;if(e.has("EXT_texture_filter_anisotropic")===!0){let B=e.get("EXT_texture_filter_anisotropic");s=i.getParameter(B.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else s=0;return s}function l(B){return!(B!==kn&&n.convert(B)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_FORMAT))}function h(B){let w=B===ei&&(e.has("EXT_color_buffer_half_float")||e.has("EXT_color_buffer_float"));return!(B!==En&&B!==Qn&&!w&&n.convert(B)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_TYPE))}function d(B){if(B==="highp"){if(i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.HIGH_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.HIGH_FLOAT).precision>0)return"highp";B="mediump"}return B==="mediump"&&i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.MEDIUM_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let f=t.precision!==void 0?t.precision:"highp",g=d(f);g!==f&&(et("WebGLRenderer:",f,"not supported, using",g,"instead."),f=g);let y=t.logarithmicDepthBuffer===!0,m=t.reversedDepthBuffer===!0&&e.has("EXT_clip_control");t.reversedDepthBuffer===!0&&m===!1&&et("WebGLRenderer: Unable to use reversed depth buffer due to missing EXT_clip_control extension. Fallback to default depth buffer.");let S=i.getParameter(i.MAX_TEXTURE_IMAGE_UNITS),T=i.getParameter(i.MAX_VERTEX_TEXTURE_IMAGE_UNITS),P=i.getParameter(i.MAX_TEXTURE_SIZE),b=i.getParameter(i.MAX_CUBE_MAP_TEXTURE_SIZE),_=i.getParameter(i.MAX_VERTEX_ATTRIBS),U=i.getParameter(i.MAX_VERTEX_UNIFORM_VECTORS),z=i.getParameter(i.MAX_VARYING_VECTORS),R=i.getParameter(i.MAX_FRAGMENT_UNIFORM_VECTORS),I=i.getParameter(i.MAX_SAMPLES),L=i.getParameter(i.SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:o,getMaxPrecision:d,textureFormatReadable:l,textureTypeReadable:h,precision:f,logarithmicDepthBuffer:y,reversedDepthBuffer:m,maxTextures:S,maxVertexTextures:T,maxTextureSize:P,maxCubemapSize:b,maxAttributes:_,maxVertexUniforms:U,maxVaryings:z,maxFragmentUniforms:R,maxSamples:I,samples:L}}function Ux(i){let e=this,t=null,n=0,s=!1,o=!1,l=new Pn,h=new at,d={value:null,needsUpdate:!1};this.uniform=d,this.numPlanes=0,this.numIntersection=0,this.init=function(y,m){let S=y.length!==0||m||n!==0||s;return s=m,n=y.length,S},this.beginShadows=function(){o=!0,g(null)},this.endShadows=function(){o=!1},this.setGlobalState=function(y,m){t=g(y,m,0)},this.setState=function(y,m,S){let T=y.clippingPlanes,P=y.clipIntersection,b=y.clipShadows,_=i.get(y);if(!s||T===null||T.length===0||o&&!b)o?g(null):f();else{let U=o?0:n,z=U*4,R=_.clippingState||null;d.value=R,R=g(T,m,z,S);for(let I=0;I!==z;++I)R[I]=t[I];_.clippingState=R,this.numIntersection=P?this.numPlanes:0,this.numPlanes+=U}};function f(){d.value!==t&&(d.value=t,d.needsUpdate=n>0),e.numPlanes=n,e.numIntersection=0}function g(y,m,S,T){let P=y!==null?y.length:0,b=null;if(P!==0){if(b=d.value,T!==!0||b===null){let _=S+P*4,U=m.matrixWorldInverse;h.getNormalMatrix(U),(b===null||b.length<_)&&(b=new Float32Array(_));for(let z=0,R=S;z!==P;++z,R+=4)l.copy(y[z]).applyMatrix4(U,h),l.normal.toArray(b,R),b[R+3]=l.constant}d.value=b,d.needsUpdate=!0}return e.numPlanes=P,e.numIntersection=0,b}}var Yr=4,Ox=6,Bx=20,kx=256,Vs=new Vr,od=new ht,kc=null,zc=0,Vc=0,Gc=!1,zx=new j,cr=new j,cl=class{constructor(e){this._renderer=e,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._sizeLods=[],this._lodMeshes=[],this._backgroundBox=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._blurMaterial=null,this._ggxMaterial=null}fromScene(e,t=0,n=.1,s=100,o={}){let{size:l=256,position:h=zx}=o;kc=this._renderer.getRenderTarget(),zc=this._renderer.getActiveCubeFace(),Vc=this._renderer.getActiveMipmapLevel(),Gc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(l);let d=this._allocateTargets();return d.depthBuffer=!0,this._sceneToCubeUV(e,n,s,d,h),t>0&&this._blur(d,0,0,t),this._applyPMREM(d),this._cleanup(d),d}fromEquirectangular(e,t=null){return this._fromTexture(e,t)}fromCubemap(e,t=null){return this._fromTexture(e,t)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=hd(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=cd(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose(),this._backgroundBox!==null&&(this._backgroundBox.geometry.dispose(),this._backgroundBox.material.dispose())}_setSize(e){this._lodMax=Math.floor(Math.log2(e)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._ggxMaterial!==null&&this._ggxMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let e=0;e<this._lodMeshes.length;e++)this._lodMeshes[e].geometry.dispose()}_cleanup(e){this._renderer.setRenderTarget(kc,zc,Vc),this._renderer.xr.enabled=Gc,e.scissorTest=!1,qr(e,0,0,e.width,e.height)}_fromTexture(e,t){e.mapping===zi||e.mapping===or?this._setSize(e.image.length===0?16:e.image[0].width||e.image[0].image.width):this._setSize(e.image.width/4),kc=this._renderer.getRenderTarget(),zc=this._renderer.getActiveCubeFace(),Vc=this._renderer.getActiveMipmapLevel(),Gc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;let n=t||this._allocateTargets();return this._textureToCubeUV(e,n),this._applyPMREM(n),this._cleanup(n),n}_allocateTargets(){let e=3*Math.max(this._cubeSize,112),t=4*this._cubeSize,n={magFilter:ln,minFilter:ln,generateMipmaps:!1,type:ei,format:kn,colorSpace:us,depthBuffer:!1},s=ld(e,t,n);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==e||this._pingPongRenderTarget.height!==t){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=ld(e,t,n);let{_lodMax:o}=this;({lodMeshes:this._lodMeshes,sizeLods:this._sizeLods}=Vx(o)),this._blurMaterial=Hx(o,e,t),this._ggxMaterial=Gx(o,e,t)}return s}_compileMaterial(e){let t=new yn(new Yt,e);this._renderer.compile(t,Vs)}_sceneToCubeUV(e,t,n,s,o){let d=new fn(90,1,t,n),f=[1,-1,1,1,1,1],g=[1,1,1,-1,-1,-1],y=this._renderer,m=y.autoClear,S=y.toneMapping;y.getClearColor(od),y.toneMapping=Jn,y.autoClear=!1,y.state.buffers.depth.getReversed()&&(y.setRenderTarget(s),y.clearDepth(),y.setRenderTarget(null)),this._backgroundBox===null&&(this._backgroundBox=new yn(new Fi,new Or({name:"PMREM.Background",side:xn,depthWrite:!1,depthTest:!1})));let P=this._backgroundBox,b=P.material,_=!1,U=e.background;U?U.isColor&&(b.color.copy(U),e.background=null,_=!0):(b.color.copy(od),_=!0);for(let z=0;z<6;z++){let R=z%3;R===0?(d.up.set(0,f[z],0),d.position.set(o.x,o.y,o.z),d.lookAt(o.x+g[z],o.y,o.z)):R===1?(d.up.set(0,0,f[z]),d.position.set(o.x,o.y,o.z),d.lookAt(o.x,o.y+g[z],o.z)):(d.up.set(0,f[z],0),d.position.set(o.x,o.y,o.z),d.lookAt(o.x,o.y,o.z+g[z]));let I=this._cubeSize;qr(s,R*I,z>2?I:0,I,I),y.setRenderTarget(s),_&&y.render(P,d),y.render(e,d)}y.toneMapping=S,y.autoClear=m,e.background=U}_textureToCubeUV(e,t){let n=this._renderer,s=e.mapping===zi||e.mapping===or;s?(this._cubemapMaterial===null&&(this._cubemapMaterial=hd()),this._cubemapMaterial.uniforms.flipEnvMap.value=e.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=cd());let o=s?this._cubemapMaterial:this._equirectMaterial,l=this._lodMeshes[0];l.material=o;let h=o.uniforms;h.envMap.value=e;let d=this._cubeSize;qr(t,0,0,3*d,2*d),n.setRenderTarget(t),n.render(l,Vs)}_applyPMREM(e){let t=this._renderer,n=t.autoClear;t.autoClear=!1;let s=this._lodMeshes.length;for(let o=1;o<s;o++)this._applyGGXFilter(e,o-1,o);t.autoClear=n}_applyGGXFilter(e,t,n){let s=this._renderer,o=this._pingPongRenderTarget,l=this._ggxMaterial,h=this._lodMeshes[n];h.material=l;let d=l.uniforms,f=n/(this._lodMeshes.length-1),g=t/(this._lodMeshes.length-1),y=Math.sqrt(f*f-g*g),m=f*1.25,S=y*m,{_lodMax:T}=this,P=this._sizeLods[n],b=3*P*(n>T-Yr?n-T+Yr:0),_=4*(this._cubeSize-P);d.envMap.value=e.texture,d.roughness.value=S,d.mipInt.value=T-t,qr(o,b,_,3*P,2*P),s.setRenderTarget(o),s.render(h,Vs),d.envMap.value=o.texture,d.roughness.value=0,d.mipInt.value=T-n,qr(e,b,_,3*P,2*P),s.setRenderTarget(e),s.render(h,Vs)}_blur(e,t,n,s){let o=this._pingPongRenderTarget,l=Math.min(s,Math.PI)/Math.SQRT2;this._blurPass(e,o,t,n,l),this._blurPass(o,e,n,n,l)}_blurPass(e,t,n,s,o){let l=this._renderer,h=this._blurMaterial,d=this._lodMeshes[s];d.material=h;let f=h.uniforms;f.envMap.value=e.texture,f.sigma.value=o,f.mipInt.value=this._lodMax-n;let g=this._sizeLods[s],y=3*g*(s>this._lodMax-Yr?s-this._lodMax+Yr:0),m=4*(this._cubeSize-g);qr(t,y,m,3*g,2*g),l.setRenderTarget(t),l.render(d,Vs)}};function Vx(i){let e=[],t=[],n=i,s=i-Yr+1+Ox;for(let o=0;o<s;o++){let l=Math.pow(2,n);e.push(l);let h=1/(l-2),d=-h,f=1+h,g=[d,d,f,d,f,f,d,d,f,f,d,f],y=6,m=6,S=3,T=new Float32Array(S*m*y),P=new Float32Array(S*m*y);for(let _=0;_<y;_++){let U=_%3*2/3-1,z=_>2?0:-1,R=[U,z,0,U+2/3,z,0,U+2/3,z+1,0,U,z,0,U+2/3,z+1,0,U,z+1,0];T.set(R,S*m*_);for(let I=0;I<m;I++){let L=g[I*2]*2-1,B=g[I*2+1]*2-1;_===0?cr.set(1,B,L):_===1?cr.set(-L,1,-B):_===2?cr.set(-L,B,1):_===3?cr.set(-1,B,-L):_===4?cr.set(-L,-1,B):cr.set(L,B,-1),cr.toArray(P,(_*m+I)*S)}}let b=new Yt;b.setAttribute("position",new vn(T,S)),b.setAttribute("outputDirection",new vn(P,S)),t.push(new yn(b,null)),n>Yr&&n--}return{lodMeshes:t,sizeLods:e}}function ld(i,e,t){let n=new Mn(i,e,t);return n.texture.mapping=Ls,n.texture.name="PMREM.cubeUv",n.scissorTest=!0,n}function qr(i,e,t,n,s){i.viewport.set(e,t,n,s),i.scissor.set(e,t,n,s)}function Gx(i,e,t){return new Dn({name:"PMREMGGXConvolution",defines:{GGX_SAMPLES:kx,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},roughness:{value:0},mipInt:{value:0}},vertexShader:dl(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float roughness;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359

			// Van der Corput radical inverse
			float radicalInverse_VdC(uint bits) {
				bits = (bits << 16u) | (bits >> 16u);
				bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
				bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
				bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
				bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
				return float(bits) * 2.3283064365386963e-10; // / 0x100000000
			}

			// Hammersley sequence
			vec2 hammersley(uint i, uint N) {
				return vec2(float(i) / float(N), radicalInverse_VdC(i));
			}

			// GGX VNDF importance sampling (Eric Heitz 2018)
			// "Sampling the GGX Distribution of Visible Normals"
			// https://jcgt.org/published/0007/04/01/
			vec3 importanceSampleGGX_VNDF(vec2 Xi, vec3 V, float roughness) {
				float alpha = roughness * roughness;

				// Section 4.1: Orthonormal basis
				vec3 T1 = vec3(1.0, 0.0, 0.0);
				vec3 T2 = cross(V, T1);

				// Section 4.2: Parameterization of projected area
				float r = sqrt(Xi.x);
				float phi = 2.0 * PI * Xi.y;
				float t1 = r * cos(phi);
				float t2 = r * sin(phi);
				float s = 0.5 * (1.0 + V.z);
				t2 = (1.0 - s) * sqrt(1.0 - t1 * t1) + s * t2;

				// Section 4.3: Reprojection onto hemisphere
				vec3 Nh = t1 * T1 + t2 * T2 + sqrt(max(0.0, 1.0 - t1 * t1 - t2 * t2)) * V;

				// Section 3.4: Transform back to ellipsoid configuration
				return normalize(vec3(alpha * Nh.x, alpha * Nh.y, max(0.0, Nh.z)));
			}

			void main() {
				vec3 N = normalize(vOutputDirection);
				vec3 V = N; // Assume view direction equals normal for pre-filtering

				vec3 prefilteredColor = vec3(0.0);
				float totalWeight = 0.0;

				// For very low roughness, just sample the environment directly
				if (roughness < 0.001) {
					gl_FragColor = vec4(bilinearCubeUV(envMap, N, mipInt), 1.0);
					return;
				}

				// Tangent space basis for VNDF sampling
				vec3 up = abs(N.z) < 0.999 ? vec3(0.0, 0.0, 1.0) : vec3(1.0, 0.0, 0.0);
				vec3 tangent = normalize(cross(up, N));
				vec3 bitangent = cross(N, tangent);

				for(uint i = 0u; i < uint(GGX_SAMPLES); i++) {
					vec2 Xi = hammersley(i, uint(GGX_SAMPLES));

					// For PMREM, V = N, so in tangent space V is always (0, 0, 1)
					vec3 H_tangent = importanceSampleGGX_VNDF(Xi, vec3(0.0, 0.0, 1.0), roughness);

					// Transform H back to world space
					vec3 H = normalize(tangent * H_tangent.x + bitangent * H_tangent.y + N * H_tangent.z);
					vec3 L = normalize(2.0 * dot(V, H) * H - V);

					float NdotL = max(dot(N, L), 0.0);

					if(NdotL > 0.0) {
						// Sample environment at fixed mip level
						// VNDF importance sampling handles the distribution filtering
						vec3 sampleColor = bilinearCubeUV(envMap, L, mipInt);

						// Weight by NdotL for the split-sum approximation
						// VNDF PDF naturally accounts for the visible microfacet distribution
						prefilteredColor += sampleColor * NdotL;
						totalWeight += NdotL;
					}
				}

				if (totalWeight > 0.0) {
					prefilteredColor = prefilteredColor / totalWeight;
				}

				gl_FragColor = vec4(prefilteredColor, 1.0);
			}
		`,blending:hi,depthTest:!1,depthWrite:!1})}function Hx(i,e,t){return new Dn({name:"SphericalGaussianBlur",defines:{SAMPLES:Bx,CUBEUV_TEXEL_WIDTH:1/e,CUBEUV_TEXEL_HEIGHT:1/t,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},sigma:{value:0},mipInt:{value:0}},vertexShader:dl(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float sigma;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359
			#define GOLDEN_ANGLE 2.39996322973

			void main() {

				if ( sigma == 0.0 ) {

					gl_FragColor = vec4( bilinearCubeUV( envMap, vOutputDirection, mipInt ), 1.0 );
					return;

				}

				vec3 outputDirection = normalize( vOutputDirection );

				vec3 up = abs( outputDirection.z ) < 0.999 ? vec3( 0.0, 0.0, 1.0 ) : vec3( 1.0, 0.0, 0.0 );
				vec3 tangent = normalize( cross( up, outputDirection ) );
				vec3 bitangent = cross( outputDirection, tangent );

				// Truncate the kernel at three standard deviations or at the antipode.
				float thetaMax = min( 3.0 * sigma, PI );
				float truncation = 1.0 - exp( - 0.5 * thetaMax * thetaMax / ( sigma * sigma ) );

				vec3 accumColor = vec3( 0.0 );
				float accumWeight = 0.0;

				for ( int i = 0; i < SAMPLES; i ++ ) {

					// Stratified inverse-CDF sampling of the Gaussian, placed on a golden-angle spiral.
					float stratum = ( float( i ) + 0.5 ) / float( SAMPLES );
					float theta = sigma * sqrt( - 2.0 * log( 1.0 - stratum * truncation ) );
					float phi = float( i ) * GOLDEN_ANGLE;

					vec3 offset = cos( phi ) * tangent + sin( phi ) * bitangent;
					vec3 sampleDirection = cos( theta ) * outputDirection + sin( theta ) * offset;

					// Correct the planar sample density to solid angle.
					float weight = sin( theta ) / theta;

					accumColor += weight * bilinearCubeUV( envMap, sampleDirection, mipInt );
					accumWeight += weight;

				}

				gl_FragColor = vec4( accumColor / accumWeight, 1.0 );

			}
		`,blending:hi,depthTest:!1,depthWrite:!1})}function cd(){return new Dn({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:dl(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:hi,depthTest:!1,depthWrite:!1})}function hd(){return new Dn({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:dl(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:hi,depthTest:!1,depthWrite:!1})}function dl(){return`

		precision mediump float;
		precision mediump int;

		attribute vec3 outputDirection;

		varying vec3 vOutputDirection;

		void main() {

			vOutputDirection = outputDirection;
			gl_Position = vec4( position, 1.0 );

		}
	`}var hl=class extends Mn{constructor(e=1,t={}){super(e,e,t),this.isWebGLCubeRenderTarget=!0;let n={width:e,height:e,depth:1},s=[n,n,n,n,n,n];this.texture=new ys(s),this._setTextureOptions(t),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(e,t){this.texture.type=t.type,this.texture.colorSpace=t.colorSpace,this.texture.generateMipmaps=t.generateMipmaps,this.texture.minFilter=t.minFilter,this.texture.magFilter=t.magFilter;let n={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},s=new Fi(5,5,5),o=new Dn({name:"CubemapFromEquirect",uniforms:lr(n.uniforms),vertexShader:n.vertexShader,fragmentShader:n.fragmentShader,side:xn,blending:hi});o.uniforms.tEquirect.value=t;let l=new yn(s,o),h=t.minFilter;return t.minFilter===Vi&&(t.minFilter=ln),new go(1,10,this).update(e,l),t.minFilter=h,l.geometry.dispose(),l.material.dispose(),this}clear(e,t=!0,n=!0,s=!0){let o=e.getRenderTarget();for(let l=0;l<6;l++)e.setRenderTarget(this,l),e.clear(t,n,s);e.setRenderTarget(o)}};function Wx(i){let e=new WeakMap,t=new WeakMap,n=null;function s(m,S=!1){return m==null?null:S?l(m):o(m)}function o(m){if(m&&m.isTexture){let S=m.mapping;if(S===yo||S===xo)if(e.has(m)){let T=e.get(m).texture;return h(T,m.mapping)}else{let T=m.image;if(T&&T.height>0){let P=new hl(T.height);return P.fromEquirectangularTexture(i,m),e.set(m,P),m.addEventListener("dispose",f),h(P.texture,m.mapping)}else return null}}return m}function l(m){if(m&&m.isTexture){let S=m.mapping,T=S===yo||S===xo,P=S===zi||S===or;if(T||P){let b=t.get(m),_=b!==void 0?b.texture.pmremVersion:0;if(m.isRenderTargetTexture&&m.pmremVersion!==_)return n===null&&(n=new cl(i)),b=T?n.fromEquirectangular(m,b):n.fromCubemap(m,b),b.texture.pmremVersion=m.pmremVersion,t.set(m,b),b.texture;if(b!==void 0)return b.texture;{let U=m.image;return T&&U&&U.height>0||P&&U&&d(U)?(n===null&&(n=new cl(i)),b=T?n.fromEquirectangular(m):n.fromCubemap(m),b.texture.pmremVersion=m.pmremVersion,t.set(m,b),m.addEventListener("dispose",g),b.texture):null}}}return m}function h(m,S){return S===yo?m.mapping=zi:S===xo&&(m.mapping=or),m}function d(m){let S=0,T=6;for(let P=0;P<T;P++)m[P]!==void 0&&S++;return S===T}function f(m){let S=m.target;S.removeEventListener("dispose",f);let T=e.get(S);T!==void 0&&(e.delete(S),T.dispose())}function g(m){let S=m.target;S.removeEventListener("dispose",g);let T=t.get(S);T!==void 0&&(t.delete(S),T.dispose())}function y(){e=new WeakMap,t=new WeakMap,n!==null&&(n.dispose(),n=null)}return{get:s,dispose:y}}function Xx(i){let e={};function t(n){if(e[n]!==void 0)return e[n];let s=i.getExtension(n);return e[n]=s,s}return{has:function(n){return t(n)!==null},init:function(){t("EXT_color_buffer_float"),t("WEBGL_clip_cull_distance"),t("OES_texture_float_linear"),t("EXT_color_buffer_half_float"),t("WEBGL_multisampled_render_to_texture"),t("WEBGL_render_shared_exponent")},get:function(n){let s=t(n);return s===null&&nr("WebGLRenderer: "+n+" extension not supported."),s}}}function $x(i,e,t,n){let s={},o=new WeakMap;function l(y){let m=y.target;m.index!==null&&e.remove(m.index);for(let T in m.attributes)e.remove(m.attributes[T]);m.removeEventListener("dispose",l),delete s[m.id];let S=o.get(m);S&&(e.remove(S),o.delete(m)),n.releaseStatesOfGeometry(m),m.isInstancedBufferGeometry===!0&&delete m._maxInstanceCount,t.memory.geometries--}function h(y,m){return s[m.id]===!0||(m.addEventListener("dispose",l),s[m.id]=!0,t.memory.geometries++),m}function d(y){let m=y.attributes;for(let S in m)e.update(m[S],i.ARRAY_BUFFER)}function f(y){let m=[],S=y.index,T=y.attributes.position,P=0;if(T===void 0)return;if(S!==null){let U=S.array;P=S.version;for(let z=0,R=U.length;z<R;z+=3){let I=U[z+0],L=U[z+1],B=U[z+2];m.push(I,L,L,B,B,I)}}else{let U=T.array;P=T.version;for(let z=0,R=U.length/3-1;z<R;z+=3){let I=z+0,L=z+1,B=z+2;m.push(I,L,L,B,B,I)}}let b=new(T.count>=65535?_s:gs)(m,1);b.version=P;let _=o.get(y);_&&e.remove(_),o.set(y,b)}function g(y){let m=o.get(y);if(m){let S=y.index;S!==null&&m.version<S.version&&f(y)}else f(y);return o.get(y)}return{get:h,update:d,getWireframeAttribute:g}}function jx(i,e,t){let n;function s(y){n=y}let o,l;function h(y){o=y.type,l=y.bytesPerElement}function d(y,m){i.drawElements(n,m,o,y*l),t.update(m,n,1)}function f(y,m,S){S!==0&&(i.drawElementsInstanced(n,m,o,y*l,S),t.update(m,n,S))}function g(y,m,S){if(S===0)return;e.get("WEBGL_multi_draw").multiDrawElementsWEBGL(n,m,0,o,y,0,S);let P=0;for(let b=0;b<S;b++)P+=m[b];t.update(P,n,1)}this.setMode=s,this.setIndex=h,this.render=d,this.renderInstances=f,this.renderMultiDraw=g}function qx(i){let e={geometries:0,textures:0},t={frame:0,calls:0,triangles:0,points:0,lines:0};function n(o,l,h){switch(t.calls++,l){case i.TRIANGLES:t.triangles+=h*(o/3);break;case i.LINES:t.lines+=h*(o/2);break;case i.LINE_STRIP:t.lines+=h*(o-1);break;case i.LINE_LOOP:t.lines+=h*o;break;case i.POINTS:t.points+=h*o;break;default:it("WebGLInfo: Unknown draw mode:",l);break}}function s(){t.calls=0,t.triangles=0,t.points=0,t.lines=0}return{memory:e,render:t,programs:null,autoReset:!0,reset:s,update:n}}function Yx(i,e,t){let n=new WeakMap,s=new Ht;function o(l,h,d){let f=l.morphTargetInfluences,g=h.morphAttributes.position||h.morphAttributes.normal||h.morphAttributes.color,y=g!==void 0?g.length:0,m=n.get(h);if(m===void 0||m.count!==y){let D=function(){B.dispose(),n.delete(h),h.removeEventListener("dispose",D)};m!==void 0&&m.texture.dispose();let S=h.morphAttributes.position!==void 0,T=h.morphAttributes.normal!==void 0,P=h.morphAttributes.color!==void 0,b=h.morphAttributes.position||[],_=h.morphAttributes.normal||[],U=h.morphAttributes.color||[],z=0;S===!0&&(z=1),T===!0&&(z=2),P===!0&&(z=3);let R=h.attributes.position.count*z,I=1;R>e.maxTextureSize&&(I=Math.ceil(R/e.maxTextureSize),R=e.maxTextureSize);let L=new Float32Array(R*I*4*y),B=new ps(L,R,I,y);B.type=Qn,B.needsUpdate=!0;let w=z*4;for(let O=0;O<y;O++){let q=b[O],Y=_[O],J=U[O],H=R*I*4*O;for(let te=0;te<q.count;te++){let k=te*w;S===!0&&(s.fromBufferAttribute(q,te),L[H+k+0]=s.x,L[H+k+1]=s.y,L[H+k+2]=s.z,L[H+k+3]=0),T===!0&&(s.fromBufferAttribute(Y,te),L[H+k+4]=s.x,L[H+k+5]=s.y,L[H+k+6]=s.z,L[H+k+7]=0),P===!0&&(s.fromBufferAttribute(J,te),L[H+k+8]=s.x,L[H+k+9]=s.y,L[H+k+10]=s.z,L[H+k+11]=J.itemSize===4?s.w:1)}}m={count:y,texture:B,size:new nt(R,I)},n.set(h,m),h.addEventListener("dispose",D)}if(l.isInstancedMesh===!0&&l.morphTexture!==null)d.getUniforms().setValue(i,"morphTexture",l.morphTexture,t);else{let S=0;for(let P=0;P<f.length;P++)S+=f[P];let T=h.morphTargetsRelative?1:1-S;d.getUniforms().setValue(i,"morphTargetBaseInfluence",T),d.getUniforms().setValue(i,"morphTargetInfluences",f)}d.getUniforms().setValue(i,"morphTargetsTexture",m.texture,t),d.getUniforms().setValue(i,"morphTargetsTextureSize",m.size)}return{update:o}}function Zx(i,e,t,n,s){let o=new WeakMap;function l(f){let g=s.render.frame,y=f.geometry,m=e.get(f,y);if(o.get(m)!==g&&(e.update(m),o.set(m,g)),f.isInstancedMesh&&(f.hasEventListener("dispose",d)===!1&&f.addEventListener("dispose",d),o.get(f)!==g&&(t.update(f.instanceMatrix,i.ARRAY_BUFFER),f.instanceColor!==null&&t.update(f.instanceColor,i.ARRAY_BUFFER),o.set(f,g))),f.isSkinnedMesh){let S=f.skeleton;o.get(S)!==g&&(S.update(),o.set(S,g))}return m}function h(){o=new WeakMap}function d(f){let g=f.target;g.removeEventListener("dispose",d),n.releaseStatesOfObject(g),t.remove(g.instanceMatrix),g.instanceColor!==null&&t.remove(g.instanceColor)}return{update:l,dispose:h}}var Jx={[gc]:"LINEAR_TONE_MAPPING",[_c]:"REINHARD_TONE_MAPPING",[vc]:"CINEON_TONE_MAPPING",[yc]:"ACES_FILMIC_TONE_MAPPING",[Sc]:"AGX_TONE_MAPPING",[bc]:"NEUTRAL_TONE_MAPPING",[xc]:"CUSTOM_TONE_MAPPING"};function Kx(i,e,t,n,s,o){let l=new Mn(e,t,{type:i,depthBuffer:s,stencilBuffer:o,samples:n?4:0,storeMultisampledDepthBuffer:!1,storeMultisampledStencilBuffer:!1,resolveDepthBuffer:!1,resolveStencilBuffer:!1}),h=null,d=null,f=new Yt;f.setAttribute("position",new zt([-1,3,0,-1,-1,0,3,-1,0],3)),f.setAttribute("uv",new zt([0,2,0,0,2,0],2));let g=new to({uniforms:{tDiffuse:{value:null}},vertexShader:`
			precision highp float;

			uniform mat4 modelViewMatrix;
			uniform mat4 projectionMatrix;

			attribute vec3 position;
			attribute vec2 uv;

			varying vec2 vUv;

			void main() {
				vUv = uv;
				gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			}`,fragmentShader:`
			precision highp float;

			uniform sampler2D tDiffuse;

			varying vec2 vUv;

			#include <tonemapping_pars_fragment>
			#include <colorspace_pars_fragment>

			void main() {
				gl_FragColor = texture2D( tDiffuse, vUv );

				#ifdef LINEAR_TONE_MAPPING
					gl_FragColor.rgb = LinearToneMapping( gl_FragColor.rgb );
				#elif defined( REINHARD_TONE_MAPPING )
					gl_FragColor.rgb = ReinhardToneMapping( gl_FragColor.rgb );
				#elif defined( CINEON_TONE_MAPPING )
					gl_FragColor.rgb = CineonToneMapping( gl_FragColor.rgb );
				#elif defined( ACES_FILMIC_TONE_MAPPING )
					gl_FragColor.rgb = ACESFilmicToneMapping( gl_FragColor.rgb );
				#elif defined( AGX_TONE_MAPPING )
					gl_FragColor.rgb = AgXToneMapping( gl_FragColor.rgb );
				#elif defined( NEUTRAL_TONE_MAPPING )
					gl_FragColor.rgb = NeutralToneMapping( gl_FragColor.rgb );
				#elif defined( CUSTOM_TONE_MAPPING )
					gl_FragColor.rgb = CustomToneMapping( gl_FragColor.rgb );
				#endif

				#ifdef SRGB_TRANSFER
					gl_FragColor = sRGBTransferOETF( gl_FragColor );
				#endif
			}`,depthTest:!1,depthWrite:!1}),y=new yn(f,g),m=new Vr(-1,1,1,-1,0,1),S=null,T=null,P=!1,b,_=null,U=[],z=!1;this.setSize=function(R,I){l.setSize(R,I),h!==null&&h.setSize(R,I),d!==null&&d.setSize(R,I);for(let L=0;L<U.length;L++){let B=U[L];B.setSize&&B.setSize(R,I)}},this.setEffects=function(R){U=R,z=U.length>0&&U[0].isRenderPass===!0;let I=l.width,L=l.height;U.length>0&&h===null&&(h=new Mn(I,L,{type:ei,depthBuffer:!1,stencilBuffer:!1}),d=new Mn(I,L,{type:ei,depthBuffer:!1,stencilBuffer:!1}));for(let B=0;B<U.length;B++){let w=U[B];w.setSize&&w.setSize(I,L)}},this.begin=function(R,I){if(P||R.toneMapping===Jn&&U.length===0)return!1;if(_=I,I!==null){let L=I.width,B=I.height;(l.width!==L||l.height!==B)&&this.setSize(L,B)}return z===!1&&R.setRenderTarget(l),b=R.toneMapping,R.toneMapping=Jn,!0},this.hasRenderPass=function(){return z},this.end=function(R,I){R.toneMapping=b,P=!0;let L=l,B=h;for(let w=0;w<U.length;w++){let D=U[w];D.enabled!==!1&&(D.render(R,B,L,I),D.needsSwap!==!1&&(L=B,B=B===h?d:h))}if(S!==R.outputColorSpace||T!==R.toneMapping){S=R.outputColorSpace,T=R.toneMapping,g.defines={},xt.getTransfer(S)===It&&(g.defines.SRGB_TRANSFER="");let w=Jx[T];w&&(g.defines[w]=""),g.needsUpdate=!0}g.uniforms.tDiffuse.value=L.texture,R.setRenderTarget(_),R.render(y,m),_=null,P=!1},this.isCompositing=function(){return P},this.dispose=function(){l.dispose(),h!==null&&h.dispose(),d!==null&&d.dispose(),f.dispose(),g.dispose()}}var Pd=new bn,Xc=new Li(1,1),Id=new ps,Dd=new qa,Ld=new ys,ud=[],dd=[],fd=new Float32Array(16),pd=new Float32Array(9),md=new Float32Array(4);function Jr(i,e,t){let n=i[0];if(n<=0||n>0)return i;let s=e*t,o=ud[s];if(o===void 0&&(o=new Float32Array(s),ud[s]=o),e!==0){n.toArray(o,0);for(let l=1,h=0;l!==e;++l)h+=t,i[l].toArray(o,h)}return o}function Qt(i,e){if(i.length!==e.length)return!1;for(let t=0,n=i.length;t<n;t++)if(i[t]!==e[t])return!1;return!0}function en(i,e){for(let t=0,n=e.length;t<n;t++)i[t]=e[t]}function fl(i,e){let t=dd[e];t===void 0&&(t=new Int32Array(e),dd[e]=t);for(let n=0;n!==e;++n)t[n]=i.allocateTextureUnit();return t}function Qx(i,e){let t=this.cache;t[0]!==e&&(i.uniform1f(this.addr,e),t[0]=e)}function eS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(i.uniform2f(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Qt(t,e))return;i.uniform2fv(this.addr,e),en(t,e)}}function tS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(i.uniform3f(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else if(e.r!==void 0)(t[0]!==e.r||t[1]!==e.g||t[2]!==e.b)&&(i.uniform3f(this.addr,e.r,e.g,e.b),t[0]=e.r,t[1]=e.g,t[2]=e.b);else{if(Qt(t,e))return;i.uniform3fv(this.addr,e),en(t,e)}}function nS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(i.uniform4f(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Qt(t,e))return;i.uniform4fv(this.addr,e),en(t,e)}}function iS(i,e){let t=this.cache,n=e.elements;if(n===void 0){if(Qt(t,e))return;i.uniformMatrix2fv(this.addr,!1,e),en(t,e)}else{if(Qt(t,n))return;md.set(n),i.uniformMatrix2fv(this.addr,!1,md),en(t,n)}}function rS(i,e){let t=this.cache,n=e.elements;if(n===void 0){if(Qt(t,e))return;i.uniformMatrix3fv(this.addr,!1,e),en(t,e)}else{if(Qt(t,n))return;pd.set(n),i.uniformMatrix3fv(this.addr,!1,pd),en(t,n)}}function sS(i,e){let t=this.cache,n=e.elements;if(n===void 0){if(Qt(t,e))return;i.uniformMatrix4fv(this.addr,!1,e),en(t,e)}else{if(Qt(t,n))return;fd.set(n),i.uniformMatrix4fv(this.addr,!1,fd),en(t,n)}}function aS(i,e){let t=this.cache;t[0]!==e&&(i.uniform1i(this.addr,e),t[0]=e)}function oS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(i.uniform2i(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Qt(t,e))return;i.uniform2iv(this.addr,e),en(t,e)}}function lS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(i.uniform3i(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Qt(t,e))return;i.uniform3iv(this.addr,e),en(t,e)}}function cS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(i.uniform4i(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Qt(t,e))return;i.uniform4iv(this.addr,e),en(t,e)}}function hS(i,e){let t=this.cache;t[0]!==e&&(i.uniform1ui(this.addr,e),t[0]=e)}function uS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y)&&(i.uniform2ui(this.addr,e.x,e.y),t[0]=e.x,t[1]=e.y);else{if(Qt(t,e))return;i.uniform2uiv(this.addr,e),en(t,e)}}function dS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z)&&(i.uniform3ui(this.addr,e.x,e.y,e.z),t[0]=e.x,t[1]=e.y,t[2]=e.z);else{if(Qt(t,e))return;i.uniform3uiv(this.addr,e),en(t,e)}}function fS(i,e){let t=this.cache;if(e.x!==void 0)(t[0]!==e.x||t[1]!==e.y||t[2]!==e.z||t[3]!==e.w)&&(i.uniform4ui(this.addr,e.x,e.y,e.z,e.w),t[0]=e.x,t[1]=e.y,t[2]=e.z,t[3]=e.w);else{if(Qt(t,e))return;i.uniform4uiv(this.addr,e),en(t,e)}}function pS(i,e,t){let n=this.cache,s=t.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s);let o;this.type===i.SAMPLER_2D_SHADOW?(Xc.compareFunction=t.isReversedDepthBuffer()?al:sl,o=Xc):o=Pd,t.setTexture2D(e||o,s)}function mS(i,e,t){let n=this.cache,s=t.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),t.setTexture3D(e||Dd,s)}function gS(i,e,t){let n=this.cache,s=t.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),t.setTextureCube(e||Ld,s)}function _S(i,e,t){let n=this.cache,s=t.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),t.setTexture2DArray(e||Id,s)}function vS(i){switch(i){case 5126:return Qx;case 35664:return eS;case 35665:return tS;case 35666:return nS;case 35674:return iS;case 35675:return rS;case 35676:return sS;case 5124:case 35670:return aS;case 35667:case 35671:return oS;case 35668:case 35672:return lS;case 35669:case 35673:return cS;case 5125:return hS;case 36294:return uS;case 36295:return dS;case 36296:return fS;case 35678:case 36198:case 36298:case 36306:case 35682:return pS;case 35679:case 36299:case 36307:return mS;case 35680:case 36300:case 36308:case 36293:return gS;case 36289:case 36303:case 36311:case 36292:return _S}}function yS(i,e){i.uniform1fv(this.addr,e)}function xS(i,e){let t=Jr(e,this.size,2);i.uniform2fv(this.addr,t)}function SS(i,e){let t=Jr(e,this.size,3);i.uniform3fv(this.addr,t)}function bS(i,e){let t=Jr(e,this.size,4);i.uniform4fv(this.addr,t)}function MS(i,e){let t=Jr(e,this.size,4);i.uniformMatrix2fv(this.addr,!1,t)}function ES(i,e){let t=Jr(e,this.size,9);i.uniformMatrix3fv(this.addr,!1,t)}function wS(i,e){let t=Jr(e,this.size,16);i.uniformMatrix4fv(this.addr,!1,t)}function TS(i,e){i.uniform1iv(this.addr,e)}function AS(i,e){i.uniform2iv(this.addr,e)}function CS(i,e){i.uniform3iv(this.addr,e)}function RS(i,e){i.uniform4iv(this.addr,e)}function PS(i,e){i.uniform1uiv(this.addr,e)}function IS(i,e){i.uniform2uiv(this.addr,e)}function DS(i,e){i.uniform3uiv(this.addr,e)}function LS(i,e){i.uniform4uiv(this.addr,e)}function FS(i,e,t){let n=this.cache,s=e.length,o=fl(t,s);Qt(n,o)||(i.uniform1iv(this.addr,o),en(n,o));let l;this.type===i.SAMPLER_2D_SHADOW?l=Xc:l=Pd;for(let h=0;h!==s;++h)t.setTexture2D(e[h]||l,o[h])}function NS(i,e,t){let n=this.cache,s=e.length,o=fl(t,s);Qt(n,o)||(i.uniform1iv(this.addr,o),en(n,o));for(let l=0;l!==s;++l)t.setTexture3D(e[l]||Dd,o[l])}function US(i,e,t){let n=this.cache,s=e.length,o=fl(t,s);Qt(n,o)||(i.uniform1iv(this.addr,o),en(n,o));for(let l=0;l!==s;++l)t.setTextureCube(e[l]||Ld,o[l])}function OS(i,e,t){let n=this.cache,s=e.length,o=fl(t,s);Qt(n,o)||(i.uniform1iv(this.addr,o),en(n,o));for(let l=0;l!==s;++l)t.setTexture2DArray(e[l]||Id,o[l])}function BS(i){switch(i){case 5126:return yS;case 35664:return xS;case 35665:return SS;case 35666:return bS;case 35674:return MS;case 35675:return ES;case 35676:return wS;case 5124:case 35670:return TS;case 35667:case 35671:return AS;case 35668:case 35672:return CS;case 35669:case 35673:return RS;case 5125:return PS;case 36294:return IS;case 36295:return DS;case 36296:return LS;case 35678:case 36198:case 36298:case 36306:case 35682:return FS;case 35679:case 36299:case 36307:return NS;case 35680:case 36300:case 36308:case 36293:return US;case 36289:case 36303:case 36311:case 36292:return OS}}var $c=class{constructor(e,t,n){this.id=e,this.addr=n,this.cache=[],this.type=t.type,this.setValue=vS(t.type)}},jc=class{constructor(e,t,n){this.id=e,this.addr=n,this.cache=[],this.type=t.type,this.size=t.size,this.setValue=BS(t.type)}},qc=class{constructor(e){this.id=e,this.seq=[],this.map={}}setValue(e,t,n){let s=this.seq;for(let o=0,l=s.length;o!==l;++o){let h=s[o];h.setValue(e,t[h.id],n)}}},Hc=/(\w+)(\])?(\[|\.)?/g;function gd(i,e){i.seq.push(e),i.map[e.id]=e}function kS(i,e,t){let n=i.name,s=n.length;for(Hc.lastIndex=0;;){let o=Hc.exec(n),l=Hc.lastIndex,h=o[1],d=o[2]==="]",f=o[3];if(d&&(h=h|0),f===void 0||f==="["&&l+2===s){gd(t,f===void 0?new $c(h,i,e):new jc(h,i,e));break}else{let y=t.map[h];y===void 0&&(y=new qc(h),gd(t,y)),t=y}}}var Zr=class{constructor(e,t){this.seq=[],this.map={};let n=e.getProgramParameter(t,e.ACTIVE_UNIFORMS);for(let l=0;l<n;++l){let h=e.getActiveUniform(t,l),d=e.getUniformLocation(t,h.name);kS(h,d,this)}let s=[],o=[];for(let l of this.seq)l.type===e.SAMPLER_2D_SHADOW||l.type===e.SAMPLER_CUBE_SHADOW||l.type===e.SAMPLER_2D_ARRAY_SHADOW?s.push(l):o.push(l);s.length>0&&(this.seq=s.concat(o))}setValue(e,t,n,s){let o=this.map[t];o!==void 0&&o.setValue(e,n,s)}setOptional(e,t,n){let s=t[n];s!==void 0&&this.setValue(e,n,s)}static upload(e,t,n,s){for(let o=0,l=t.length;o!==l;++o){let h=t[o],d=n[h.id];d.needsUpdate!==!1&&h.setValue(e,d.value,s)}}static seqWithValue(e,t){let n=[];for(let s=0,o=e.length;s!==o;++s){let l=e[s];l.id in t&&n.push(l)}return n}};function _d(i,e,t){let n=i.createShader(e);return i.shaderSource(n,t),i.compileShader(n),n}var zS=37297,VS=0;function GS(i,e){let t=i.split(`
`),n=[],s=Math.max(e-6,0),o=Math.min(e+6,t.length);for(let l=s;l<o;l++){let h=l+1;n.push(`${h===e?">":" "} ${h}: ${t[l]}`)}return n.join(`
`)}var vd=new at;function HS(i){xt._getMatrix(vd,xt.workingColorSpace,i);let e=`mat3( ${vd.elements.map(t=>t.toFixed(4))} )`;switch(xt.getTransfer(i)){case ds:return[e,"LinearTransferOETF"];case It:return[e,"sRGBTransferOETF"];default:return et("WebGLProgram: Unsupported color space: ",i),[e,"LinearTransferOETF"]}}function yd(i,e,t){let n=i.getShaderParameter(e,i.COMPILE_STATUS),o=(i.getShaderInfoLog(e)||"").trim();if(n&&o==="")return"";let l=/ERROR: 0:(\d+)/.exec(o);if(l){let h=parseInt(l[1]);return t.toUpperCase()+`

`+o+`

`+GS(i.getShaderSource(e),h)}else return o}function WS(i,e){let t=HS(e);return[`vec4 ${i}( vec4 value ) {`,`	return ${t[1]}( vec4( value.rgb * ${t[0]}, value.a ) );`,"}"].join(`
`)}var XS={[gc]:"Linear",[_c]:"Reinhard",[vc]:"Cineon",[yc]:"ACESFilmic",[Sc]:"AgX",[bc]:"Neutral",[xc]:"Custom"};function $S(i,e){let t=XS[e];return t===void 0?(et("WebGLProgram: Unsupported toneMapping:",e),"vec3 "+i+"( vec3 color ) { return LinearToneMapping( color ); }"):"vec3 "+i+"( vec3 color ) { return "+t+"ToneMapping( color ); }"}var ll=new j;function jS(){xt.getLuminanceCoefficients(ll);let i=ll.x.toFixed(4),e=ll.y.toFixed(4),t=ll.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${i}, ${e}, ${t} );`,"	return dot( weights, rgb );","}"].join(`
`)}function qS(i){return[i.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",i.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Hs).join(`
`)}function YS(i){let e=[];for(let t in i){let n=i[t];n!==!1&&e.push("#define "+t+" "+n)}return e.join(`
`)}function ZS(i,e){let t={},n=i.getProgramParameter(e,i.ACTIVE_ATTRIBUTES);for(let s=0;s<n;s++){let o=i.getActiveAttrib(e,s),l=o.name,h=1;o.type===i.FLOAT_MAT2&&(h=2),o.type===i.FLOAT_MAT3&&(h=3),o.type===i.FLOAT_MAT4&&(h=4),t[l]={type:o.type,location:i.getAttribLocation(e,l),locationSize:h}}return t}function Hs(i){return i!==""}function xd(i,e){let t=e.numSpotLightShadows+e.numSpotLightMaps-e.numSpotLightShadowsWithMaps;return i.replace(/NUM_SUN_LIGHTS/g,e.numSunLights).replace(/NUM_DIR_LIGHTS/g,e.numDirLights).replace(/NUM_SPOT_LIGHTS/g,e.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,e.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,t).replace(/NUM_RECT_AREA_LIGHTS/g,e.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,e.numPointLights).replace(/NUM_HEMI_LIGHTS/g,e.numHemiLights).replace(/NUM_SUN_LIGHT_SHADOWS/g,e.numSunLightShadows).replace(/NUM_DIR_LIGHT_SHADOWS/g,e.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,e.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,e.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,e.numPointLightShadows)}function Sd(i,e){return i.replace(/NUM_CLIPPING_PLANES/g,e.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,e.numClippingPlanes-e.numClipIntersection)}var JS=/^[ \t]*#include +<([\w\d./]+)>/gm;function Yc(i){return i.replace(JS,QS)}var KS=new Map;function QS(i,e){let t=pt[e];if(t===void 0){let n=KS.get(e);if(n!==void 0)t=pt[n],et('WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',e,n);else throw new Error("THREE.WebGLProgram: Can not resolve #include <"+e+">")}return Yc(t)}var eb=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function bd(i){return i.replace(eb,tb)}function tb(i,e,t,n){let s="";for(let o=parseInt(e);o<parseInt(t);o++)s+=n.replace(/\[\s*i\s*\]/g,"[ "+o+" ]").replace(/UNROLLED_LOOP_INDEX/g,o);return s}function Md(i){let e=`precision ${i.precision} float;
	precision ${i.precision} int;
	precision ${i.precision} sampler2D;
	precision ${i.precision} samplerCube;
	precision ${i.precision} sampler3D;
	precision ${i.precision} sampler2DArray;
	precision ${i.precision} sampler2DShadow;
	precision ${i.precision} samplerCubeShadow;
	precision ${i.precision} sampler2DArrayShadow;
	precision ${i.precision} isampler2D;
	precision ${i.precision} isampler3D;
	precision ${i.precision} isamplerCube;
	precision ${i.precision} isampler2DArray;
	precision ${i.precision} usampler2D;
	precision ${i.precision} usampler3D;
	precision ${i.precision} usamplerCube;
	precision ${i.precision} usampler2DArray;
	`;return i.precision==="highp"?e+=`
#define HIGH_PRECISION`:i.precision==="mediump"?e+=`
#define MEDIUM_PRECISION`:i.precision==="lowp"&&(e+=`
#define LOW_PRECISION`),e}var nb={[Ds]:"SHADOWMAP_TYPE_PCF",[Hr]:"SHADOWMAP_TYPE_VSM"};function ib(i){return nb[i.shadowMapType]||"SHADOWMAP_TYPE_BASIC"}var rb={[zi]:"ENVMAP_TYPE_CUBE",[or]:"ENVMAP_TYPE_CUBE",[Ls]:"ENVMAP_TYPE_CUBE_UV"};function sb(i){return i.envMap===!1?"ENVMAP_TYPE_CUBE":rb[i.envMapMode]||"ENVMAP_TYPE_CUBE"}var ab={[or]:"ENVMAP_MODE_REFRACTION"};function ob(i){return i.envMap===!1?"ENVMAP_MODE_REFLECTION":ab[i.envMapMode]||"ENVMAP_MODE_REFLECTION"}var lb={[vo]:"ENVMAP_BLENDING_MULTIPLY",[zu]:"ENVMAP_BLENDING_MIX",[Vu]:"ENVMAP_BLENDING_ADD"};function cb(i){return i.envMap===!1?"ENVMAP_BLENDING_NONE":lb[i.combine]||"ENVMAP_BLENDING_NONE"}function hb(i){let e=i.envMapCubeUVHeight;if(e===null)return null;let t=Math.log2(e)-2,n=1/e;return{texelWidth:1/(3*Math.max(Math.pow(2,t),112)),texelHeight:n,maxMip:t}}function ub(i,e,t,n){let s=i.getContext(),o=t.defines,l=t.vertexShader,h=t.fragmentShader,d=ib(t),f=sb(t),g=ob(t),y=cb(t),m=hb(t),S=qS(t),T=YS(o),P=s.createProgram(),b,_,U=t.glslVersion?"#version "+t.glslVersion+`
`:"";t.isRawShaderMaterial?(b=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,T].filter(Hs).join(`
`),b.length>0&&(b+=`
`),_=["#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,T].filter(Hs).join(`
`),_.length>0&&(_+=`
`)):(b=[Md(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,T,t.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",t.batching?"#define USE_BATCHING":"",t.batchingColor?"#define USE_BATCHING_COLOR":"",t.instancing?"#define USE_INSTANCING":"",t.instancingColor?"#define USE_INSTANCING_COLOR":"",t.instancingMorph?"#define USE_INSTANCING_MORPH":"",t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.map?"#define USE_MAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+g:"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.displacementMap?"#define USE_DISPLACEMENTMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.mapUv?"#define MAP_UV "+t.mapUv:"",t.alphaMapUv?"#define ALPHAMAP_UV "+t.alphaMapUv:"",t.lightMapUv?"#define LIGHTMAP_UV "+t.lightMapUv:"",t.aoMapUv?"#define AOMAP_UV "+t.aoMapUv:"",t.emissiveMapUv?"#define EMISSIVEMAP_UV "+t.emissiveMapUv:"",t.bumpMapUv?"#define BUMPMAP_UV "+t.bumpMapUv:"",t.normalMapUv?"#define NORMALMAP_UV "+t.normalMapUv:"",t.displacementMapUv?"#define DISPLACEMENTMAP_UV "+t.displacementMapUv:"",t.metalnessMapUv?"#define METALNESSMAP_UV "+t.metalnessMapUv:"",t.roughnessMapUv?"#define ROUGHNESSMAP_UV "+t.roughnessMapUv:"",t.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+t.anisotropyMapUv:"",t.clearcoatMapUv?"#define CLEARCOATMAP_UV "+t.clearcoatMapUv:"",t.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+t.clearcoatNormalMapUv:"",t.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+t.clearcoatRoughnessMapUv:"",t.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+t.iridescenceMapUv:"",t.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+t.iridescenceThicknessMapUv:"",t.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+t.sheenColorMapUv:"",t.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+t.sheenRoughnessMapUv:"",t.specularMapUv?"#define SPECULARMAP_UV "+t.specularMapUv:"",t.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+t.specularColorMapUv:"",t.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+t.specularIntensityMapUv:"",t.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+t.transmissionMapUv:"",t.thicknessMapUv?"#define THICKNESSMAP_UV "+t.thicknessMapUv:"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexNormals?"#define HAS_NORMAL":"",t.vertexColors?"#define USE_COLOR":"",t.vertexAlphas?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.flatShading?"#define FLAT_SHADED":"",t.skinning?"#define USE_SKINNING":"",t.morphTargets?"#define USE_MORPHTARGETS":"",t.morphNormals&&t.flatShading===!1?"#define USE_MORPHNORMALS":"",t.morphColors?"#define USE_MORPHCOLORS":"",t.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+t.morphTextureStride:"",t.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+t.morphTargetsCount:"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+d:"",t.sizeAttenuation?"#define USE_SIZEATTENUATION":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",t.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Hs).join(`
`),_=[Md(t),"#define SHADER_TYPE "+t.shaderType,"#define SHADER_NAME "+t.shaderName,T,t.useFog&&t.fog?"#define USE_FOG":"",t.useFog&&t.fogExp2?"#define FOG_EXP2":"",t.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",t.map?"#define USE_MAP":"",t.matcap?"#define USE_MATCAP":"",t.envMap?"#define USE_ENVMAP":"",t.envMap?"#define "+f:"",t.envMap?"#define "+g:"",t.envMap?"#define "+y:"",m?"#define CUBEUV_TEXEL_WIDTH "+m.texelWidth:"",m?"#define CUBEUV_TEXEL_HEIGHT "+m.texelHeight:"",m?"#define CUBEUV_MAX_MIP "+m.maxMip+".0":"",t.lightMap?"#define USE_LIGHTMAP":"",t.aoMap?"#define USE_AOMAP":"",t.bumpMap?"#define USE_BUMPMAP":"",t.normalMap?"#define USE_NORMALMAP":"",t.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",t.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",t.packedNormalMap?"#define USE_PACKED_NORMALMAP":"",t.emissiveMap?"#define USE_EMISSIVEMAP":"",t.anisotropy?"#define USE_ANISOTROPY":"",t.anisotropyMap?"#define USE_ANISOTROPYMAP":"",t.clearcoat?"#define USE_CLEARCOAT":"",t.clearcoatMap?"#define USE_CLEARCOATMAP":"",t.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",t.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",t.dispersion?"#define USE_DISPERSION":"",t.retroreflection?"#define USE_RETROREFLECTION":"",t.iridescence?"#define USE_IRIDESCENCE":"",t.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",t.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",t.specularMap?"#define USE_SPECULARMAP":"",t.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",t.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",t.roughnessMap?"#define USE_ROUGHNESSMAP":"",t.metalnessMap?"#define USE_METALNESSMAP":"",t.alphaMap?"#define USE_ALPHAMAP":"",t.alphaTest?"#define USE_ALPHATEST":"",t.alphaHash?"#define USE_ALPHAHASH":"",t.sheen?"#define USE_SHEEN":"",t.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",t.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",t.transmission?"#define USE_TRANSMISSION":"",t.transmissionMap?"#define USE_TRANSMISSIONMAP":"",t.thicknessMap?"#define USE_THICKNESSMAP":"",t.vertexTangents&&t.flatShading===!1?"#define USE_TANGENT":"",t.vertexColors||t.instancingColor?"#define USE_COLOR":"",t.vertexAlphas||t.batchingColor?"#define USE_COLOR_ALPHA":"",t.vertexUv1s?"#define USE_UV1":"",t.vertexUv2s?"#define USE_UV2":"",t.vertexUv3s?"#define USE_UV3":"",t.pointsUvs?"#define USE_POINTS_UV":"",t.gradientMap?"#define USE_GRADIENTMAP":"",t.flatShading?"#define FLAT_SHADED":"",t.doubleSided?"#define DOUBLE_SIDED":"",t.flipSided?"#define FLIP_SIDED":"",t.shadowMapEnabled?"#define USE_SHADOWMAP":"",t.shadowMapEnabled?"#define "+d:"",t.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",t.numLightProbes>0?"#define USE_LIGHT_PROBES":"",t.numLightProbeGrids>0?"#define USE_LIGHT_PROBES_GRID":"",t.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",t.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",t.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",t.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",t.toneMapping!==Jn?"#define TONE_MAPPING":"",t.toneMapping!==Jn?pt.tonemapping_pars_fragment:"",t.toneMapping!==Jn?$S("toneMapping",t.toneMapping):"",t.dithering?"#define DITHERING":"",t.opaque?"#define OPAQUE":"",pt.colorspace_pars_fragment,WS("linearToOutputTexel",t.outputColorSpace),jS(),t.useDepthPacking?"#define DEPTH_PACKING "+t.depthPacking:"",`
`].filter(Hs).join(`
`)),l=Yc(l),l=xd(l,t),l=Sd(l,t),h=Yc(h),h=xd(h,t),h=Sd(h,t),l=bd(l),h=bd(h),t.isRawShaderMaterial!==!0&&(U=`#version 300 es
`,b=[S,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+b,_=["#define varying in",t.glslVersion===Ic?"":"layout(location = 0) out highp vec4 pc_fragColor;",t.glslVersion===Ic?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+_);let z=U+b+l,R=U+_+h,I=_d(s,s.VERTEX_SHADER,z),L=_d(s,s.FRAGMENT_SHADER,R);s.attachShader(P,I),s.attachShader(P,L),t.index0AttributeName!==void 0?s.bindAttribLocation(P,0,t.index0AttributeName):t.hasPositionAttribute===!0&&s.bindAttribLocation(P,0,"position"),s.linkProgram(P);function B(q){if(i.debug.checkShaderErrors){let Y=s.getProgramInfoLog(P)||"",J=s.getShaderInfoLog(I)||"",H=s.getShaderInfoLog(L)||"",te=Y.trim(),k=J.trim(),se=H.trim(),_e=!0,ae=!0;if(s.getProgramParameter(P,s.LINK_STATUS)===!1)if(_e=!1,typeof i.debug.onShaderError=="function")i.debug.onShaderError(s,P,I,L);else{let V=yd(s,I,"vertex"),ge=yd(s,L,"fragment");it("WebGLProgram: Shader Error "+s.getError()+" - VALIDATE_STATUS "+s.getProgramParameter(P,s.VALIDATE_STATUS)+`

Material Name: `+q.name+`
Material Type: `+q.type+`

Program Info Log: `+te+`
`+V+`
`+ge)}else te!==""?et("WebGLProgram: Program Info Log:",te):(k===""||se==="")&&(ae=!1);ae&&(q.diagnostics={runnable:_e,programLog:te,vertexShader:{log:k,prefix:b},fragmentShader:{log:se,prefix:_}})}s.deleteShader(I),s.deleteShader(L),w=new Zr(s,P),D=ZS(s,P)}let w;this.getUniforms=function(){return w===void 0&&B(this),w};let D;this.getAttributes=function(){return D===void 0&&B(this),D};let O=t.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return O===!1&&(O=s.getProgramParameter(P,zS)),O},this.destroy=function(){n.releaseStatesOfProgram(this),s.deleteProgram(P),this.program=void 0},this.type=t.shaderType,this.name=t.shaderName,this.id=VS++,this.cacheKey=e,this.usedTimes=1,this.program=P,this.vertexShader=I,this.fragmentShader=L,this}var db=0,Zc=class{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(e,t,n){let s=this._getShaderCacheForMaterial(e);return s.has(t)===!1&&(s.add(t),t.usedTimes++),s.has(n)===!1&&(s.add(n),n.usedTimes++),this}remove(e){let t=this.materialCache.get(e);for(let n of t)n.usedTimes--,n.usedTimes===0&&this.shaderCache.delete(n.code);return this.materialCache.delete(e),this}getVertexShaderStage(e){return this._getShaderStage(e.vertexShader)}getFragmentShaderStage(e){return this._getShaderStage(e.fragmentShader)}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(e){let t=this.materialCache,n=t.get(e);return n===void 0&&(n=new Set,t.set(e,n)),n}_getShaderStage(e){let t=this.shaderCache,n=t.get(e);return n===void 0&&(n=new Jc(e),t.set(e,n)),n}},Jc=class{constructor(e){this.id=db++,this.code=e,this.usedTimes=0}};function fb(i){return i===Hi||i===ks||i===zs}function pb(i,e,t,n,s,o){let l=new Nr,h=new Zc,d=new Set,f=[],g=new Map,y=n.logarithmicDepthBuffer,m=n.precision,S={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distance",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function T(w){return d.add(w),w===0?"uv":`uv${w}`}function P(w,D,O,q,Y,J){let H=q.fog,te=Y.geometry,k=w.isMeshStandardMaterial||w.isMeshLambertMaterial||w.isMeshPhongMaterial?q.environment:null,se=w.isMeshStandardMaterial||w.isMeshLambertMaterial&&!w.envMap||w.isMeshPhongMaterial&&!w.envMap,_e=e.get(w.envMap||k,se),ae=_e&&_e.mapping===Ls?_e.image.height:null,V=S[w.type];w.precision!==null&&(m=n.getMaxPrecision(w.precision),m!==w.precision&&et("WebGLProgram.getParameters:",w.precision,"not supported, using",m,"instead."));let ge=te.morphAttributes.position||te.morphAttributes.normal||te.morphAttributes.color,Ye=ge!==void 0?ge.length:0,$e=0;te.morphAttributes.position!==void 0&&($e=1),te.morphAttributes.normal!==void 0&&($e=2),te.morphAttributes.color!==void 0&&($e=3);let Ut,mt,Ke,le;if(V){let Ft=di[V];Ut=Ft.vertexShader,mt=Ft.fragmentShader}else{Ut=w.vertexShader,mt=w.fragmentShader;let Ft=h.getVertexShaderStage(w),wt=h.getFragmentShaderStage(w);h.update(w,Ft,wt),Ke=Ft.id,le=wt.id}let fe=i.getRenderTarget(),ke=i.state.buffers.depth.getReversed(),st=Y.isInstancedMesh===!0,Be=Y.isBatchedMesh===!0,ut=!!w.map,$t=!!w.matcap,dt=!!_e,gt=!!w.aoMap,rt=!!w.lightMap,tt=!!w.bumpMap&&w.wireframe===!1,St=!!w.normalMap,Bt=!!w.displacementMap,Ie=!!w.emissiveMap,Ue=!!w.metalnessMap,Vt=!!w.roughnessMap,W=w.anisotropy>0,Dt=w.clearcoat>0,Ct=w.dispersion>0,F=w.retroreflectivity>0,x=w.iridescence>0,Z=w.sheen>0,ne=w.transmission>0,oe=W&&!!w.anisotropyMap,Ee=Dt&&!!w.clearcoatMap,Ae=Dt&&!!w.clearcoatNormalMap,re=Dt&&!!w.clearcoatRoughnessMap,he=x&&!!w.iridescenceMap,Ce=x&&!!w.iridescenceThicknessMap,Xe=Z&&!!w.sheenColorMap,xe=Z&&!!w.sheenRoughnessMap,Te=!!w.specularMap,He=!!w.specularColorMap,Je=!!w.specularIntensityMap,ot=ne&&!!w.transmissionMap,X=ne&&!!w.thicknessMap,Re=!!w.gradientMap,de=!!w.alphaMap,Pe=w.alphaTest>0,Ne=!!w.alphaHash,me=!!w.extensions,je=Jn;w.toneMapped&&(fe===null||fe.isXRRenderTarget===!0)&&(je=i.toneMapping);let We={shaderID:V,shaderType:w.type,shaderName:w.name,vertexShader:Ut,fragmentShader:mt,defines:w.defines,customVertexShaderID:Ke,customFragmentShaderID:le,isRawShaderMaterial:w.isRawShaderMaterial===!0,glslVersion:w.glslVersion,precision:m,batching:Be,batchingColor:Be&&Y._colorsTexture!==null,instancing:st,instancingColor:st&&Y.instanceColor!==null,instancingMorph:st&&Y.morphTexture!==null,outputColorSpace:fe===null?i.outputColorSpace:fe.isXRRenderTarget===!0?fe.texture.colorSpace:xt.workingColorSpace,alphaToCoverage:!!w.alphaToCoverage,map:ut,matcap:$t,envMap:dt,envMapMode:dt&&_e.mapping,envMapCubeUVHeight:ae,aoMap:gt,lightMap:rt,bumpMap:tt,normalMap:St,displacementMap:Bt,emissiveMap:Ie,normalMapObjectSpace:St&&w.normalMapType===Wu,normalMapTangentSpace:St&&w.normalMapType===rl,packedNormalMap:St&&w.normalMapType===rl&&fb(w.normalMap.format),metalnessMap:Ue,roughnessMap:Vt,anisotropy:W,anisotropyMap:oe,clearcoat:Dt,clearcoatMap:Ee,clearcoatNormalMap:Ae,clearcoatRoughnessMap:re,dispersion:Ct,retroreflection:F,iridescence:x,iridescenceMap:he,iridescenceThicknessMap:Ce,sheen:Z,sheenColorMap:Xe,sheenRoughnessMap:xe,specularMap:Te,specularColorMap:He,specularIntensityMap:Je,transmission:ne,transmissionMap:ot,thicknessMap:X,gradientMap:Re,opaque:w.transparent===!1&&w.blending===Wr&&w.alphaToCoverage===!1,alphaMap:de,alphaTest:Pe,alphaHash:Ne,combine:w.combine,mapUv:ut&&T(w.map.channel),aoMapUv:gt&&T(w.aoMap.channel),lightMapUv:rt&&T(w.lightMap.channel),bumpMapUv:tt&&T(w.bumpMap.channel),normalMapUv:St&&T(w.normalMap.channel),displacementMapUv:Bt&&T(w.displacementMap.channel),emissiveMapUv:Ie&&T(w.emissiveMap.channel),metalnessMapUv:Ue&&T(w.metalnessMap.channel),roughnessMapUv:Vt&&T(w.roughnessMap.channel),anisotropyMapUv:oe&&T(w.anisotropyMap.channel),clearcoatMapUv:Ee&&T(w.clearcoatMap.channel),clearcoatNormalMapUv:Ae&&T(w.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:re&&T(w.clearcoatRoughnessMap.channel),iridescenceMapUv:he&&T(w.iridescenceMap.channel),iridescenceThicknessMapUv:Ce&&T(w.iridescenceThicknessMap.channel),sheenColorMapUv:Xe&&T(w.sheenColorMap.channel),sheenRoughnessMapUv:xe&&T(w.sheenRoughnessMap.channel),specularMapUv:Te&&T(w.specularMap.channel),specularColorMapUv:He&&T(w.specularColorMap.channel),specularIntensityMapUv:Je&&T(w.specularIntensityMap.channel),transmissionMapUv:ot&&T(w.transmissionMap.channel),thicknessMapUv:X&&T(w.thicknessMap.channel),alphaMapUv:de&&T(w.alphaMap.channel),vertexTangents:!!te.attributes.tangent&&(St||W),vertexNormals:!!te.attributes.normal,vertexColors:w.vertexColors,vertexAlphas:w.vertexColors===!0&&!!te.attributes.color&&te.attributes.color.itemSize===4,pointsUvs:Y.isPoints===!0&&!!te.attributes.uv&&(ut||de),fog:!!H,useFog:w.fog===!0,fogExp2:!!H&&H.isFogExp2,flatShading:w.wireframe===!1&&(w.flatShading===!0||te.attributes.normal===void 0&&St===!1&&(w.isMeshLambertMaterial||w.isMeshPhongMaterial||w.isMeshStandardMaterial||w.isMeshPhysicalMaterial)),sizeAttenuation:w.sizeAttenuation===!0,logarithmicDepthBuffer:y,reversedDepthBuffer:ke,skinning:Y.isSkinnedMesh===!0,hasPositionAttribute:te.attributes.position!==void 0,morphTargets:te.morphAttributes.position!==void 0,morphNormals:te.morphAttributes.normal!==void 0,morphColors:te.morphAttributes.color!==void 0,morphTargetsCount:Ye,morphTextureStride:$e,numSunLights:D.sun.length,numDirLights:D.directional.length,numPointLights:D.point.length,numSpotLights:D.spot.length,numSpotLightMaps:D.spotLightMap.length,numRectAreaLights:D.rectArea.length,numHemiLights:D.hemi.length,numSunLightShadows:D.sunShadowMap.length,numDirLightShadows:D.directionalShadowMap.length,numPointLightShadows:D.pointShadowMap.length,numSpotLightShadows:D.spotShadowMap.length,numSpotLightShadowsWithMaps:D.numSpotLightShadowsWithMaps,numLightProbes:D.numLightProbes,numLightProbeGrids:J.length,numClippingPlanes:o.numPlanes,numClipIntersection:o.numIntersection,dithering:w.dithering,shadowMapEnabled:i.shadowMap.enabled&&O.length>0,shadowMapType:i.shadowMap.type,toneMapping:je,decodeVideoTexture:ut&&w.map.isVideoTexture===!0&&xt.getTransfer(w.map.colorSpace)===It,decodeVideoTextureEmissive:Ie&&w.emissiveMap.isVideoTexture===!0&&xt.getTransfer(w.emissiveMap.colorSpace)===It,premultipliedAlpha:w.premultipliedAlpha,doubleSided:w.side===ci,flipSided:w.side===xn,useDepthPacking:w.depthPacking>=0,depthPacking:w.depthPacking||0,index0AttributeName:w.index0AttributeName,extensionClipCullDistance:me&&w.extensions.clipCullDistance===!0&&t.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(me&&w.extensions.multiDraw===!0||Be)&&t.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:t.has("KHR_parallel_shader_compile"),customProgramCacheKey:w.customProgramCacheKey()};return We.vertexUv1s=d.has(1),We.vertexUv2s=d.has(2),We.vertexUv3s=d.has(3),d.clear(),We}function b(w){let D=[];if(w.shaderID?D.push(w.shaderID):(D.push(w.customVertexShaderID),D.push(w.customFragmentShaderID)),w.defines!==void 0)for(let O in w.defines)D.push(O),D.push(w.defines[O]);return w.isRawShaderMaterial===!1&&(_(D,w),U(D,w),D.push(i.outputColorSpace)),D.push(w.customProgramCacheKey),D.join()}function _(w,D){w.push(D.precision),w.push(D.outputColorSpace),w.push(D.envMapMode),w.push(D.envMapCubeUVHeight),w.push(D.mapUv),w.push(D.alphaMapUv),w.push(D.lightMapUv),w.push(D.aoMapUv),w.push(D.bumpMapUv),w.push(D.normalMapUv),w.push(D.displacementMapUv),w.push(D.emissiveMapUv),w.push(D.metalnessMapUv),w.push(D.roughnessMapUv),w.push(D.anisotropyMapUv),w.push(D.clearcoatMapUv),w.push(D.clearcoatNormalMapUv),w.push(D.clearcoatRoughnessMapUv),w.push(D.iridescenceMapUv),w.push(D.iridescenceThicknessMapUv),w.push(D.sheenColorMapUv),w.push(D.sheenRoughnessMapUv),w.push(D.specularMapUv),w.push(D.specularColorMapUv),w.push(D.specularIntensityMapUv),w.push(D.transmissionMapUv),w.push(D.thicknessMapUv),w.push(D.combine),w.push(D.fogExp2),w.push(D.sizeAttenuation),w.push(D.morphTargetsCount),w.push(D.morphAttributeCount),w.push(D.numSunLights),w.push(D.numDirLights),w.push(D.numPointLights),w.push(D.numSpotLights),w.push(D.numSpotLightMaps),w.push(D.numHemiLights),w.push(D.numRectAreaLights),w.push(D.numSunLightShadows),w.push(D.numDirLightShadows),w.push(D.numPointLightShadows),w.push(D.numSpotLightShadows),w.push(D.numSpotLightShadowsWithMaps),w.push(D.numLightProbes),w.push(D.shadowMapType),w.push(D.toneMapping),w.push(D.numClippingPlanes),w.push(D.numClipIntersection),w.push(D.depthPacking)}function U(w,D){l.disableAll(),D.instancing&&l.enable(0),D.instancingColor&&l.enable(1),D.instancingMorph&&l.enable(2),D.matcap&&l.enable(3),D.envMap&&l.enable(4),D.normalMapObjectSpace&&l.enable(5),D.normalMapTangentSpace&&l.enable(6),D.clearcoat&&l.enable(7),D.iridescence&&l.enable(8),D.alphaTest&&l.enable(9),D.vertexColors&&l.enable(10),D.vertexAlphas&&l.enable(11),D.vertexUv1s&&l.enable(12),D.vertexUv2s&&l.enable(13),D.vertexUv3s&&l.enable(14),D.vertexTangents&&l.enable(15),D.anisotropy&&l.enable(16),D.alphaHash&&l.enable(17),D.batching&&l.enable(18),D.dispersion&&l.enable(19),D.retroreflection&&l.enable(24),D.batchingColor&&l.enable(20),D.gradientMap&&l.enable(21),D.packedNormalMap&&l.enable(22),D.vertexNormals&&l.enable(23),w.push(l.mask),l.disableAll(),D.fog&&l.enable(0),D.useFog&&l.enable(1),D.flatShading&&l.enable(2),D.logarithmicDepthBuffer&&l.enable(3),D.reversedDepthBuffer&&l.enable(4),D.skinning&&l.enable(5),D.morphTargets&&l.enable(6),D.morphNormals&&l.enable(7),D.morphColors&&l.enable(8),D.premultipliedAlpha&&l.enable(9),D.shadowMapEnabled&&l.enable(10),D.doubleSided&&l.enable(11),D.flipSided&&l.enable(12),D.useDepthPacking&&l.enable(13),D.dithering&&l.enable(14),D.transmission&&l.enable(15),D.sheen&&l.enable(16),D.opaque&&l.enable(17),D.pointsUvs&&l.enable(18),D.decodeVideoTexture&&l.enable(19),D.decodeVideoTextureEmissive&&l.enable(20),D.alphaToCoverage&&l.enable(21),D.numLightProbeGrids>0&&l.enable(22),D.hasPositionAttribute&&l.enable(23),w.push(l.mask)}function z(w){let D=S[w.type],O;if(D){let q=di[D];O=rd.clone(q.uniforms)}else O=w.uniforms;return O}function R(w,D){let O=g.get(D);return O!==void 0?++O.usedTimes:(O=new ub(i,D,w,s),f.push(O),g.set(D,O)),O}function I(w){if(--w.usedTimes===0){let D=f.indexOf(w);f[D]=f[f.length-1],f.pop(),g.delete(w.cacheKey),w.destroy()}}function L(w){h.remove(w)}function B(){h.dispose()}return{getParameters:P,getProgramCacheKey:b,getUniforms:z,acquireProgram:R,releaseProgram:I,releaseShaderCache:L,programs:f,dispose:B}}function mb(){let i=new WeakMap;function e(l){return i.has(l)}function t(l){let h=i.get(l);return h===void 0&&(h={},i.set(l,h)),h}function n(l){i.delete(l)}function s(l,h,d){i.get(l)[h]=d}function o(){i=new WeakMap}return{has:e,get:t,remove:n,update:s,dispose:o}}function gb(i,e){return i.groupOrder!==e.groupOrder?i.groupOrder-e.groupOrder:i.renderOrder!==e.renderOrder?i.renderOrder-e.renderOrder:i.material.id!==e.material.id?i.material.id-e.material.id:i.materialVariant!==e.materialVariant?i.materialVariant-e.materialVariant:i.z!==e.z?i.z-e.z:i.id-e.id}function Ed(i,e){return i.groupOrder!==e.groupOrder?i.groupOrder-e.groupOrder:i.renderOrder!==e.renderOrder?i.renderOrder-e.renderOrder:i.z!==e.z?e.z-i.z:i.id-e.id}function wd(){let i=[],e=0,t=[],n=[],s=[];function o(){e=0,t.length=0,n.length=0,s.length=0}function l(m){let S=0;return m.isInstancedMesh&&(S+=2),m.isSkinnedMesh&&(S+=1),S}function h(m,S,T,P,b,_){let U=i[e];return U===void 0?(U={id:m.id,object:m,geometry:S,material:T,materialVariant:l(m),groupOrder:P,renderOrder:m.renderOrder,z:b,group:_},i[e]=U):(U.id=m.id,U.object=m,U.geometry=S,U.material=T,U.materialVariant=l(m),U.groupOrder=P,U.renderOrder=m.renderOrder,U.z=b,U.group=_),e++,U}function d(m,S,T,P,b,_,U){U.reversedDepth===!0&&(b=-b);let z=h(m,S,T,P,b,_);T.transmission>0?n.push(z):T.transparent===!0?s.push(z):t.push(z)}function f(m,S,T,P,b,_){let U=h(m,S,T,P,b,_);T.transmission>0?n.unshift(U):T.transparent===!0?s.unshift(U):t.unshift(U)}function g(m,S){t.length>1&&t.sort(m||gb),n.length>1&&n.sort(S||Ed),s.length>1&&s.sort(S||Ed)}function y(){for(let m=e,S=i.length;m<S;m++){let T=i[m];if(T.id===null)break;T.id=null,T.object=null,T.geometry=null,T.material=null,T.group=null}}return{opaque:t,transmissive:n,transparent:s,init:o,push:d,unshift:f,finish:y,sort:g}}function _b(){let i=new WeakMap;function e(n,s){let o=i.get(n),l;return o===void 0?(l=new wd,i.set(n,[l])):s>=o.length?(l=new wd,o.push(l)):l=o[s],l}function t(){i=new WeakMap}return{get:e,dispose:t}}function vb(){let i={};return{get:function(e){if(i[e.id]!==void 0)return i[e.id];let t;switch(e.type){case"SunLight":case"DirectionalLight":t={direction:new j,color:new ht};break;case"SpotLight":t={position:new j,direction:new j,color:new ht,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":t={position:new j,color:new ht,distance:0,decay:0};break;case"HemisphereLight":t={direction:new j,skyColor:new ht,groundColor:new ht};break;case"RectAreaLight":t={color:new ht,position:new j,halfWidth:new j,halfHeight:new j};break}return i[e.id]=t,t}}}function yb(){let i={};return{get:function(e){if(i[e.id]!==void 0)return i[e.id];let t;switch(e.type){case"SunLight":case"DirectionalLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new nt};break;case"SpotLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new nt};break;case"PointLight":t={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new nt,shadowCameraNear:1,shadowCameraFar:1e3};break}return i[e.id]=t,t}}}var xb=0;function Sb(i,e){return(e.castShadow?2:0)-(i.castShadow?2:0)+(e.map?1:0)-(i.map?1:0)}function bb(i){let e=new vb,t=yb(),n={version:0,hash:{sunLength:-1,directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numSunShadows:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],sun:[],sunShadow:[],sunShadowMap:[],sunShadowMatrix:[],sunShadowCascade:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let f=0;f<9;f++)n.probe.push(new j);let s=new j,o=new Ot,l=new Ot;function h(f){let g=0,y=0,m=0;for(let Y=0;Y<9;Y++)n.probe[Y].set(0,0,0);let S=0,T=0,P=0,b=0,_=0,U=0,z=0,R=0,I=0,L=0,B=0,w=0,D=0,O=0;f.sort(Sb);for(let Y=0,J=f.length;Y<J;Y++){let H=f[Y],te=H.color,k=H.intensity,se=H.distance,_e=null;if(H.shadow&&H.shadow.map&&(H.shadow.map.texture.format===Hi?_e=H.shadow.map.texture:_e=H.shadow.map.depthTexture||H.shadow.map.texture),H.isAmbientLight)g+=te.r*k,y+=te.g*k,m+=te.b*k;else if(H.isLightProbe){for(let ae=0;ae<9;ae++)n.probe[ae].addScaledVector(H.sh.coefficients[ae],k);O++}else if(H.isSunLight){let ae=e.get(H);if(ae.color.copy(H.color).multiplyScalar(H.intensity),H.castShadow){let V=H.shadow,ge=t.get(H);ge.shadowIntensity=V.intensity,ge.shadowBias=V.bias,ge.shadowNormalBias=V.normalBias,ge.shadowRadius=V.radius,ge.shadowMapSize.copy(V.mapSize).multiply(V.getFrameExtents()),n.sunShadow[T]=ge,n.sunShadowMap[T]=_e;let Ye=V.getViewportCount();for(let $e=0;$e<Ye;$e++)n.sunShadowMatrix[P+$e]=V.getMatrix($e),n.sunShadowCascade[P+$e]=V._cascadeData[$e];P+=Ye,T++}n.sun[S]=ae,S++}else if(H.isDirectionalLight){let ae=e.get(H);if(ae.color.copy(H.color).multiplyScalar(H.intensity),H.castShadow){let V=H.shadow,ge=t.get(H);ge.shadowIntensity=V.intensity,ge.shadowBias=V.bias,ge.shadowNormalBias=V.normalBias,ge.shadowRadius=V.radius,ge.shadowMapSize=V.mapSize,n.directionalShadow[b]=ge,n.directionalShadowMap[b]=_e,n.directionalShadowMatrix[b]=H.shadow.matrix,I++}n.directional[b]=ae,b++}else if(H.isSpotLight){let ae=e.get(H);ae.position.setFromMatrixPosition(H.matrixWorld),ae.color.copy(te).multiplyScalar(k),ae.distance=se,ae.coneCos=Math.cos(H.angle),ae.penumbraCos=Math.cos(H.angle*(1-H.penumbra)),ae.decay=H.decay,n.spot[U]=ae;let V=H.shadow;if(H.map&&(n.spotLightMap[w]=H.map,w++,V.updateMatrices(H),H.castShadow&&D++),n.spotLightMatrix[U]=V.matrix,H.castShadow){let ge=t.get(H);ge.shadowIntensity=V.intensity,ge.shadowBias=V.bias,ge.shadowNormalBias=V.normalBias,ge.shadowRadius=V.radius,ge.shadowMapSize=V.mapSize,n.spotShadow[U]=ge,n.spotShadowMap[U]=_e,B++}U++}else if(H.isRectAreaLight){let ae=e.get(H);ae.color.copy(te).multiplyScalar(k),ae.halfWidth.set(H.width*.5,0,0),ae.halfHeight.set(0,H.height*.5,0),n.rectArea[z]=ae,z++}else if(H.isPointLight){let ae=e.get(H);if(ae.color.copy(H.color).multiplyScalar(H.intensity),ae.distance=H.distance,ae.decay=H.decay,H.castShadow){let V=H.shadow,ge=t.get(H);ge.shadowIntensity=V.intensity,ge.shadowBias=V.bias,ge.shadowNormalBias=V.normalBias,ge.shadowRadius=V.radius,ge.shadowMapSize=V.mapSize,ge.shadowCameraNear=V.camera.near,ge.shadowCameraFar=V.camera.far,n.pointShadow[_]=ge,n.pointShadowMap[_]=_e,n.pointShadowMatrix[_]=H.shadow.matrix,L++}n.point[_]=ae,_++}else if(H.isHemisphereLight){let ae=e.get(H);ae.skyColor.copy(H.color).multiplyScalar(k),ae.groundColor.copy(H.groundColor).multiplyScalar(k),n.hemi[R]=ae,R++}}z>0&&(i.has("OES_texture_float_linear")===!0?(n.rectAreaLTC1=Fe.LTC_FLOAT_1,n.rectAreaLTC2=Fe.LTC_FLOAT_2):(n.rectAreaLTC1=Fe.LTC_HALF_1,n.rectAreaLTC2=Fe.LTC_HALF_2)),n.ambient[0]=g,n.ambient[1]=y,n.ambient[2]=m;let q=n.hash;(q.sunLength!==S||q.directionalLength!==b||q.pointLength!==_||q.spotLength!==U||q.rectAreaLength!==z||q.hemiLength!==R||q.numSunShadows!==T||q.numDirectionalShadows!==I||q.numPointShadows!==L||q.numSpotShadows!==B||q.numSpotMaps!==w||q.numLightProbes!==O)&&(n.sun.length=S,n.directional.length=b,n.spot.length=U,n.rectArea.length=z,n.point.length=_,n.hemi.length=R,n.sunShadow.length=T,n.sunShadowMap.length=T,n.sunShadowMatrix.length=P,n.sunShadowCascade.length=P,n.directionalShadow.length=I,n.directionalShadowMap.length=I,n.directionalShadowMatrix.length=I,n.pointShadow.length=L,n.pointShadowMap.length=L,n.pointShadowMatrix.length=L,n.spotShadow.length=B,n.spotShadowMap.length=B,n.spotLightMatrix.length=B+w-D,n.spotLightMap.length=w,n.numSpotLightShadowsWithMaps=D,n.numLightProbes=O,q.sunLength=S,q.directionalLength=b,q.pointLength=_,q.spotLength=U,q.rectAreaLength=z,q.hemiLength=R,q.numSunShadows=T,q.numDirectionalShadows=I,q.numPointShadows=L,q.numSpotShadows=B,q.numSpotMaps=w,q.numLightProbes=O,n.version=xb++)}function d(f,g){let y=0,m=0,S=0,T=0,P=0,b=0,_=g.matrixWorldInverse;for(let U=0,z=f.length;U<z;U++){let R=f[U];if(R.isSunLight){let I=n.sun[y];I.direction.setFromMatrixPosition(R.matrixWorld),I.direction.transformDirection(_),y++}else if(R.isDirectionalLight){let I=n.directional[m];I.direction.setFromMatrixPosition(R.matrixWorld),s.setFromMatrixPosition(R.target.matrixWorld),I.direction.sub(s),I.direction.transformDirection(_),m++}else if(R.isSpotLight){let I=n.spot[T];I.position.setFromMatrixPosition(R.matrixWorld),I.position.applyMatrix4(_),I.direction.setFromMatrixPosition(R.matrixWorld),s.setFromMatrixPosition(R.target.matrixWorld),I.direction.sub(s),I.direction.transformDirection(_),T++}else if(R.isRectAreaLight){let I=n.rectArea[P];I.position.setFromMatrixPosition(R.matrixWorld),I.position.applyMatrix4(_),l.identity(),o.copy(R.matrixWorld),o.premultiply(_),l.extractRotation(o),I.halfWidth.set(R.width*.5,0,0),I.halfHeight.set(0,R.height*.5,0),I.halfWidth.applyMatrix4(l),I.halfHeight.applyMatrix4(l),P++}else if(R.isPointLight){let I=n.point[S];I.position.setFromMatrixPosition(R.matrixWorld),I.position.applyMatrix4(_),S++}else if(R.isHemisphereLight){let I=n.hemi[b];I.direction.setFromMatrixPosition(R.matrixWorld),I.direction.transformDirection(_),b++}}}return{setup:h,setupView:d,state:n}}function Td(i){let e=new bb(i),t=[],n=[],s=[];function o(m){y.camera=m,t.length=0,n.length=0,s.length=0}function l(m){t.push(m)}function h(m){n.push(m)}function d(m){s.push(m)}function f(){e.setup(t)}function g(m){e.setupView(t,m)}let y={lightsArray:t,shadowsArray:n,lightProbeGridArray:s,camera:null,lights:e,transmissionRenderTarget:{},textureUnits:0};return{init:o,state:y,setupLights:f,setupLightsView:g,pushLight:l,pushShadow:h,pushLightProbeGrid:d}}function Mb(i){let e=new WeakMap;function t(s,o=0){let l=e.get(s),h;return l===void 0?(h=new Td(i),e.set(s,[h])):o>=l.length?(h=new Td(i),l.push(h)):h=l[o],h}function n(){e=new WeakMap}return{get:t,dispose:n}}var Eb=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,wb=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ).rg;
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ).r;
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( max( 0.0, squared_mean - mean * mean ) );
	gl_FragColor = vec4( mean, std_dev, 0.0, 1.0 );
}`,Tb=[new j(1,0,0),new j(-1,0,0),new j(0,1,0),new j(0,-1,0),new j(0,0,1),new j(0,0,-1)],Ab=[new j(0,-1,0),new j(0,-1,0),new j(0,0,1),new j(0,0,-1),new j(0,-1,0),new j(0,-1,0)],Ad=new Ot,Gs=new j,Wc=new j;function Cb(i,e,t){let n=new Br,s=new nt,o=new nt,l=new Ht,h=new no,d=new io,f={},g=t.maxTextureSize,y={[li]:xn,[xn]:li,[ci]:ci},m=new Dn({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new nt},radius:{value:4}},vertexShader:Eb,fragmentShader:wb}),S=m.clone();S.defines.HORIZONTAL_PASS=1;let T=new Yt;T.setAttribute("position",new vn(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));let P=new yn(T,m),b=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Ds;let _=this.type;this.render=function(L,B,w){if(b.enabled===!1||b.autoUpdate===!1&&b.needsUpdate===!1||L.length===0)return;this.type===Su&&(et("WebGLShadowMap: PCFSoftShadowMap has been removed. Using PCFShadowMap instead."),this.type=Ds);let D=i.getRenderTarget(),O=i.getActiveCubeFace(),q=i.getActiveMipmapLevel(),Y=i.state;Y.setBlending(hi),Y.buffers.depth.getReversed()===!0?Y.buffers.color.setClear(0,0,0,0):Y.buffers.color.setClear(1,1,1,1),Y.buffers.depth.setTest(!0),Y.setScissorTest(!1);let J=_!==this.type;J&&B.traverse(function(H){H.material&&(Array.isArray(H.material)?H.material.forEach(te=>te.needsUpdate=!0):H.material.needsUpdate=!0)});for(let H=0,te=L.length;H<te;H++){let k=L[H],se=k.shadow;if(se===void 0){et("WebGLShadowMap:",k,"has no shadow.");continue}if(se.autoUpdate===!1&&se.needsUpdate===!1)continue;s.copy(se.mapSize);let _e=se.getFrameExtents();s.multiply(_e),o.copy(se.mapSize),(s.x>g||s.y>g)&&(s.x>g&&(o.x=Math.floor(g/_e.x),s.x=o.x*_e.x,se.mapSize.x=o.x),s.y>g&&(o.y=Math.floor(g/_e.y),s.y=o.y*_e.y,se.mapSize.y=o.y));let ae=i.state.buffers.depth.getReversed();if(se.camera._reversedDepth=ae,se.map===null||J===!0){if(se.map!==null&&(se.map.depthTexture!==null&&(se.map.depthTexture.dispose(),se.map.depthTexture=null),se.map.dispose()),this.type===Hr){if(k.isPointLight){et("WebGLShadowMap: VSM shadow maps are not supported for PointLights. Use PCF or BasicShadowMap instead.");continue}se.map=new Mn(s.x,s.y,{format:Hi,type:ei,minFilter:ln,magFilter:ln,generateMipmaps:!1}),se.map.texture.name=k.name+".shadowMap",se.map.depthTexture=new Li(s.x,s.y,Qn),se.map.depthTexture.name=k.name+".shadowMapDepth",se.map.depthTexture.format=ai,se.map.depthTexture.compareFunction=null,se.map.depthTexture.minFilter=an,se.map.depthTexture.magFilter=an}else k.isPointLight?(se.map=new hl(s.x),se.map.depthTexture=new Qa(s.x,Kn)):(se.map=new Mn(s.x,s.y),se.map.depthTexture=new Li(s.x,s.y,Kn)),se.map.depthTexture.name=k.name+".shadowMap",se.map.depthTexture.format=ai,this.type===Ds?(se.map.depthTexture.compareFunction=ae?al:sl,se.map.depthTexture.minFilter=ln,se.map.depthTexture.magFilter=ln):(se.map.depthTexture.compareFunction=null,se.map.depthTexture.minFilter=an,se.map.depthTexture.magFilter=an);se.camera.updateProjectionMatrix()}se.map.isWebGLCubeRenderTarget!==!0&&(se.map.width!==s.x||se.map.height!==s.y)&&se.map.setSize(s.x,s.y);let V=se.map.isWebGLCubeRenderTarget?6:se.getViewportCount();k.isPointLight!==!0&&se.updateMatrices(k,w);for(let ge=0;ge<V;ge++){let Ye=se.getCamera(ge);if(k.isPointLight){let $e=se.camera,Ut=se.matrix,mt=k.distance||$e.far;mt!==$e.far&&($e.far=mt,$e.updateProjectionMatrix()),Gs.setFromMatrixPosition(k.matrixWorld),$e.position.copy(Gs),Wc.copy($e.position),Wc.add(Tb[ge]),$e.up.copy(Ab[ge]),$e.lookAt(Wc),$e.updateMatrixWorld(),Ut.makeTranslation(-Gs.x,-Gs.y,-Gs.z),Ad.multiplyMatrices($e.projectionMatrix,$e.matrixWorldInverse),se._frustum.setFromProjectionMatrix(Ad,$e.coordinateSystem,$e.reversedDepth)}if(se.map.isWebGLCubeRenderTarget)i.setRenderTarget(se.map,ge),i.clear();else{ge===0&&(i.setRenderTarget(se.map),i.clear());let $e=se.getViewport(ge);l.set(o.x*$e.x,o.y*$e.y,o.x*$e.z,o.y*$e.w),Y.viewport(l)}n=se.getFrustum(ge),R(B,w,Ye,k,this.type)}se.isPointLightShadow!==!0&&this.type===Hr&&U(se,w),se.needsUpdate=!1}_=this.type,b.needsUpdate=!1,i.setRenderTarget(D,O,q)};function U(L,B){let w=e.update(P);m.defines.VSM_SAMPLES!==L.blurSamples&&(m.defines.VSM_SAMPLES=L.blurSamples,S.defines.VSM_SAMPLES=L.blurSamples,m.needsUpdate=!0,S.needsUpdate=!0),L.mapPass===null?L.mapPass=new Mn(s.x,s.y,{format:Hi,type:ei}):(L.mapPass.width!==L.map.width||L.mapPass.height!==L.map.height)&&L.mapPass.setSize(L.map.width,L.map.height),m.uniforms.shadow_pass.value=L.map.depthTexture,m.uniforms.resolution.value.set(L.map.width,L.map.height),m.uniforms.radius.value=L.radius,i.setRenderTarget(L.mapPass),i.clear(),i.renderBufferDirect(B,null,w,m,P,null),S.uniforms.shadow_pass.value=L.mapPass.texture,S.uniforms.resolution.value.set(L.map.width,L.map.height),S.uniforms.radius.value=L.radius,i.setRenderTarget(L.map),i.clear(),i.renderBufferDirect(B,null,w,S,P,null)}function z(L,B,w,D){let O=null,q=w.isPointLight===!0?L.customDistanceMaterial:L.customDepthMaterial;if(q!==void 0)O=q;else if(O=w.isPointLight===!0?d:h,i.localClippingEnabled&&B.clipShadows===!0&&Array.isArray(B.clippingPlanes)&&B.clippingPlanes.length!==0||B.displacementMap&&B.displacementScale!==0||B.alphaMap&&B.alphaTest>0||B.map&&B.alphaTest>0||B.alphaToCoverage===!0){let Y=O.uuid,J=B.uuid,H=f[Y];H===void 0&&(H={},f[Y]=H);let te=H[J];te===void 0&&(te=O.clone(),H[J]=te,B.addEventListener("dispose",I)),O=te}if(O.visible=B.visible,O.wireframe=B.wireframe,D===Hr?O.side=B.shadowSide!==null?B.shadowSide:B.side:O.side=B.shadowSide!==null?B.shadowSide:y[B.side],O.alphaMap=B.alphaMap,O.alphaTest=B.alphaToCoverage===!0?.5:B.alphaTest,O.map=B.map,O.clipShadows=B.clipShadows,O.clippingPlanes=B.clippingPlanes,O.clipIntersection=B.clipIntersection,O.displacementMap=B.displacementMap,O.displacementScale=B.displacementScale,O.displacementBias=B.displacementBias,O.wireframeLinewidth=B.wireframeLinewidth,O.linewidth=B.linewidth,w.isPointLight===!0&&O.isMeshDistanceMaterial===!0){let Y=i.properties.get(O);Y.light=w}return O}function R(L,B,w,D,O){if(L.visible===!1)return;if(L.layers.test(B.layers)&&(L.isMesh||L.isLine||L.isPoints)&&(L.castShadow||L.receiveShadow&&O===Hr)&&(!L.frustumCulled||L.intersectsFrustum(n))){L.modelViewMatrix.multiplyMatrices(w.matrixWorldInverse,L.matrixWorld);let J=e.update(L),H=L.material;if(Array.isArray(H)){let te=J.groups;for(let k=0,se=te.length;k<se;k++){let _e=te[k],ae=H[_e.materialIndex];if(ae&&ae.visible){let V=z(L,ae,D,O);L.onBeforeShadow(i,L,B,w,J,V,_e),i.renderBufferDirect(w,null,J,V,L,_e),L.onAfterShadow(i,L,B,w,J,V,_e)}}}else if(H.visible){let te=z(L,H,D,O);L.onBeforeShadow(i,L,B,w,J,te,null),i.renderBufferDirect(w,null,J,te,L,null),L.onAfterShadow(i,L,B,w,J,te,null)}}let Y=L.children;for(let J=0,H=Y.length;J<H;J++)R(Y[J],B,w,D,O)}function I(L){L.target.removeEventListener("dispose",I);for(let w in f){let D=f[w],O=L.target.uuid;O in D&&(D[O].dispose(),delete D[O])}}}function Rb(i,e){function t(){let X=!1,Re=new Ht,de=null,Pe=new Ht(0,0,0,0);return{setMask:function(Ne){de!==Ne&&!X&&(i.colorMask(Ne,Ne,Ne,Ne),de=Ne)},setLocked:function(Ne){X=Ne},setClear:function(Ne,me,je,We,Ft){Ft===!0&&(Ne*=We,me*=We,je*=We),Re.set(Ne,me,je,We),Pe.equals(Re)===!1&&(i.clearColor(Ne,me,je,We),Pe.copy(Re))},reset:function(){X=!1,de=null,Pe.set(-1,0,0,0)}}}function n(){let X=!1,Re=!1,de=null,Pe=null,Ne=null;return{setReversed:function(me){if(Re!==me){let je=e.get("EXT_clip_control");me?je.clipControlEXT(je.LOWER_LEFT_EXT,je.ZERO_TO_ONE_EXT):je.clipControlEXT(je.LOWER_LEFT_EXT,je.NEGATIVE_ONE_TO_ONE_EXT),Re=me;let We=Ne;Ne=null,this.setClear(We)}},getReversed:function(){return Re},setTest:function(me){me?fe(i.DEPTH_TEST):ke(i.DEPTH_TEST)},setMask:function(me){de!==me&&!X&&(i.depthMask(me),de=me)},setFunc:function(me){if(Re&&(me=nd[me]),Pe!==me){switch(me){case Ua:i.depthFunc(i.NEVER);break;case Oa:i.depthFunc(i.ALWAYS);break;case Ba:i.depthFunc(i.LESS);break;case Pr:i.depthFunc(i.LEQUAL);break;case ka:i.depthFunc(i.EQUAL);break;case za:i.depthFunc(i.GEQUAL);break;case Va:i.depthFunc(i.GREATER);break;case Ga:i.depthFunc(i.NOTEQUAL);break;default:i.depthFunc(i.LEQUAL)}Pe=me}},setLocked:function(me){X=me},setClear:function(me){Ne!==me&&(Ne=me,Re&&(me=1-me),i.clearDepth(me))},reset:function(){X=!1,de=null,Pe=null,Ne=null,Re=!1}}}function s(){let X=!1,Re=null,de=null,Pe=null,Ne=null,me=null,je=null,We=null,Ft=null;return{setTest:function(wt){X||(wt?fe(i.STENCIL_TEST):ke(i.STENCIL_TEST))},setMask:function(wt){Re!==wt&&!X&&(i.stencilMask(wt),Re=wt)},setFunc:function(wt,Tn,zn){(de!==wt||Pe!==Tn||Ne!==zn)&&(i.stencilFunc(wt,Tn,zn),de=wt,Pe=Tn,Ne=zn)},setOp:function(wt,Tn,zn){(me!==wt||je!==Tn||We!==zn)&&(i.stencilOp(wt,Tn,zn),me=wt,je=Tn,We=zn)},setLocked:function(wt){X=wt},setClear:function(wt){Ft!==wt&&(i.clearStencil(wt),Ft=wt)},reset:function(){X=!1,Re=null,de=null,Pe=null,Ne=null,me=null,je=null,We=null,Ft=null}}}let o=new t,l=new n,h=new s,d=new WeakMap,f=new WeakMap,g={},y={},m={},S=new WeakMap,T=[],P=null,b=!1,_=null,U=null,z=null,R=null,I=null,L=null,B=null,w=new ht(0,0,0),D=0,O=!1,q=null,Y=null,J=null,H=null,te=null,k=i.getParameter(i.MAX_COMBINED_TEXTURE_IMAGE_UNITS),se=!1,_e=0,ae=i.getParameter(i.VERSION);ae.indexOf("WebGL")!==-1?(_e=parseFloat(/^WebGL (\d)/.exec(ae)[1]),se=_e>=1):ae.indexOf("OpenGL ES")!==-1&&(_e=parseFloat(/^OpenGL ES (\d)/.exec(ae)[1]),se=_e>=2);let V=null,ge={},Ye=i.getParameter(i.SCISSOR_BOX),$e=i.getParameter(i.VIEWPORT),Ut=new Ht().fromArray(Ye),mt=new Ht().fromArray($e);function Ke(X,Re,de,Pe){let Ne=new Uint8Array(4),me=i.createTexture();i.bindTexture(X,me),i.texParameteri(X,i.TEXTURE_MIN_FILTER,i.NEAREST),i.texParameteri(X,i.TEXTURE_MAG_FILTER,i.NEAREST);for(let je=0;je<de;je++)X===i.TEXTURE_3D||X===i.TEXTURE_2D_ARRAY?i.texImage3D(Re,0,i.RGBA,1,1,Pe,0,i.RGBA,i.UNSIGNED_BYTE,Ne):i.texImage2D(Re+je,0,i.RGBA,1,1,0,i.RGBA,i.UNSIGNED_BYTE,Ne);return me}let le={};le[i.TEXTURE_2D]=Ke(i.TEXTURE_2D,i.TEXTURE_2D,1),le[i.TEXTURE_CUBE_MAP]=Ke(i.TEXTURE_CUBE_MAP,i.TEXTURE_CUBE_MAP_POSITIVE_X,6),le[i.TEXTURE_2D_ARRAY]=Ke(i.TEXTURE_2D_ARRAY,i.TEXTURE_2D_ARRAY,1,1),le[i.TEXTURE_3D]=Ke(i.TEXTURE_3D,i.TEXTURE_3D,1,1),o.setClear(0,0,0,1),l.setClear(1),h.setClear(0),fe(i.DEPTH_TEST),l.setFunc(Pr),tt(!1),St(hc),fe(i.CULL_FACE),gt(hi);function fe(X){g[X]!==!0&&(i.enable(X),g[X]=!0)}function ke(X){g[X]!==!1&&(i.disable(X),g[X]=!1)}function st(X,Re){return m[X]!==Re?(i.bindFramebuffer(X,Re),m[X]=Re,X===i.DRAW_FRAMEBUFFER&&(m[i.FRAMEBUFFER]=Re),X===i.FRAMEBUFFER&&(m[i.DRAW_FRAMEBUFFER]=Re),!0):!1}function Be(X,Re){let de=T,Pe=!1;if(X){de=S.get(Re),de===void 0&&(de=[],S.set(Re,de));let Ne=X.textures;if(de.length!==Ne.length||de[0]!==i.COLOR_ATTACHMENT0){for(let me=0,je=Ne.length;me<je;me++)de[me]=i.COLOR_ATTACHMENT0+me;de.length=Ne.length,Pe=!0}}else de[0]!==i.BACK&&(de[0]=i.BACK,Pe=!0);Pe&&i.drawBuffers(de)}function ut(X){return P!==X?(i.useProgram(X),P=X,!0):!1}let $t={[ar]:i.FUNC_ADD,[Mu]:i.FUNC_SUBTRACT,[Eu]:i.FUNC_REVERSE_SUBTRACT};$t[wu]=i.MIN,$t[Tu]=i.MAX;let dt={[Au]:i.ZERO,[Cu]:i.ONE,[Ru]:i.SRC_COLOR,[pc]:i.SRC_ALPHA,[Nu]:i.SRC_ALPHA_SATURATE,[Lu]:i.DST_COLOR,[Iu]:i.DST_ALPHA,[Pu]:i.ONE_MINUS_SRC_COLOR,[mc]:i.ONE_MINUS_SRC_ALPHA,[Fu]:i.ONE_MINUS_DST_COLOR,[Du]:i.ONE_MINUS_DST_ALPHA,[Uu]:i.CONSTANT_COLOR,[Ou]:i.ONE_MINUS_CONSTANT_COLOR,[Bu]:i.CONSTANT_ALPHA,[ku]:i.ONE_MINUS_CONSTANT_ALPHA};function gt(X,Re,de,Pe,Ne,me,je,We,Ft,wt){if(X===hi){b===!0&&(ke(i.BLEND),b=!1);return}if(b===!1&&(fe(i.BLEND),b=!0),X!==bu){if(X!==_||wt!==O){if((U!==ar||I!==ar)&&(i.blendEquation(i.FUNC_ADD),U=ar,I=ar),wt)switch(X){case Wr:i.blendFuncSeparate(i.ONE,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case uc:i.blendFunc(i.ONE,i.ONE);break;case dc:i.blendFuncSeparate(i.ZERO,i.ONE_MINUS_SRC_COLOR,i.ZERO,i.ONE);break;case fc:i.blendFuncSeparate(i.DST_COLOR,i.ONE_MINUS_SRC_ALPHA,i.ZERO,i.ONE);break;default:it("WebGLState: Invalid blending: ",X);break}else switch(X){case Wr:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case uc:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE,i.ONE,i.ONE);break;case dc:it("WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case fc:it("WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:it("WebGLState: Invalid blending: ",X);break}z=null,R=null,L=null,B=null,w.set(0,0,0),D=0,_=X,O=wt}return}Ne=Ne||Re,me=me||de,je=je||Pe,(Re!==U||Ne!==I)&&(i.blendEquationSeparate($t[Re],$t[Ne]),U=Re,I=Ne),(de!==z||Pe!==R||me!==L||je!==B)&&(i.blendFuncSeparate(dt[de],dt[Pe],dt[me],dt[je]),z=de,R=Pe,L=me,B=je),(We.equals(w)===!1||Ft!==D)&&(i.blendColor(We.r,We.g,We.b,Ft),w.copy(We),D=Ft),_=X,O=!1}function rt(X,Re){X.side===ci?ke(i.CULL_FACE):fe(i.CULL_FACE);let de=X.side===xn;Re&&(de=!de),tt(de),X.blending===Wr&&X.transparent===!1?gt(hi):gt(X.blending,X.blendEquation,X.blendSrc,X.blendDst,X.blendEquationAlpha,X.blendSrcAlpha,X.blendDstAlpha,X.blendColor,X.blendAlpha,X.premultipliedAlpha),l.setFunc(X.depthFunc),l.setTest(X.depthTest),l.setMask(X.depthWrite),o.setMask(X.colorWrite);let Pe=X.stencilWrite;h.setTest(Pe),Pe&&(h.setMask(X.stencilWriteMask),h.setFunc(X.stencilFunc,X.stencilRef,X.stencilFuncMask),h.setOp(X.stencilFail,X.stencilZFail,X.stencilZPass)),Ie(X.polygonOffset,X.polygonOffsetFactor,X.polygonOffsetUnits),X.alphaToCoverage===!0?fe(i.SAMPLE_ALPHA_TO_COVERAGE):ke(i.SAMPLE_ALPHA_TO_COVERAGE)}function tt(X){q!==X&&(X?i.frontFace(i.CW):i.frontFace(i.CCW),q=X)}function St(X){X!==yu?(fe(i.CULL_FACE),X!==Y&&(X===hc?i.cullFace(i.BACK):X===xu?i.cullFace(i.FRONT):i.cullFace(i.FRONT_AND_BACK))):ke(i.CULL_FACE),Y=X}function Bt(X){X!==J&&(se&&i.lineWidth(X),J=X)}function Ie(X,Re,de){X?(fe(i.POLYGON_OFFSET_FILL),(H!==Re||te!==de)&&(H=Re,te=de,l.getReversed()&&(Re=-Re),i.polygonOffset(Re,de))):ke(i.POLYGON_OFFSET_FILL)}function Ue(X){X?fe(i.SCISSOR_TEST):ke(i.SCISSOR_TEST)}function Vt(X){X===void 0&&(X=i.TEXTURE0+k-1),V!==X&&(i.activeTexture(X),V=X)}function W(X,Re,de){de===void 0&&(V===null?de=i.TEXTURE0+k-1:de=V);let Pe=ge[de];Pe===void 0&&(Pe={type:void 0,texture:void 0},ge[de]=Pe),(Pe.type!==X||Pe.texture!==Re)&&(V!==de&&(i.activeTexture(de),V=de),i.bindTexture(X,Re||le[X]),Pe.type=X,Pe.texture=Re)}function Dt(){let X=ge[V];X!==void 0&&X.type!==void 0&&(i.bindTexture(X.type,null),X.type=void 0,X.texture=void 0)}function Ct(){try{i.compressedTexImage2D(...arguments)}catch(X){it("WebGLState:",X)}}function F(){try{i.compressedTexImage3D(...arguments)}catch(X){it("WebGLState:",X)}}function x(){try{i.texSubImage2D(...arguments)}catch(X){it("WebGLState:",X)}}function Z(){try{i.texSubImage3D(...arguments)}catch(X){it("WebGLState:",X)}}function ne(){try{i.compressedTexSubImage2D(...arguments)}catch(X){it("WebGLState:",X)}}function oe(){try{i.compressedTexSubImage3D(...arguments)}catch(X){it("WebGLState:",X)}}function Ee(){try{i.texStorage2D(...arguments)}catch(X){it("WebGLState:",X)}}function Ae(){try{i.texStorage3D(...arguments)}catch(X){it("WebGLState:",X)}}function re(){try{i.texImage2D(...arguments)}catch(X){it("WebGLState:",X)}}function he(){try{i.texImage3D(...arguments)}catch(X){it("WebGLState:",X)}}function Ce(X){return y[X]!==void 0?y[X]:i.getParameter(X)}function Xe(X,Re){y[X]!==Re&&(i.pixelStorei(X,Re),y[X]=Re)}function xe(X){Ut.equals(X)===!1&&(i.scissor(X.x,X.y,X.z,X.w),Ut.copy(X))}function Te(X){mt.equals(X)===!1&&(i.viewport(X.x,X.y,X.z,X.w),mt.copy(X))}function He(X,Re){let de=f.get(Re);de===void 0&&(de=new WeakMap,f.set(Re,de));let Pe=de.get(X);Pe===void 0&&(Pe=i.getUniformBlockIndex(Re,X.name),de.set(X,Pe))}function Je(X,Re){let Pe=f.get(Re).get(X);d.get(Re)!==Pe&&(i.uniformBlockBinding(Re,Pe,X.__bindingPointIndex),d.set(Re,Pe))}function ot(){i.disable(i.BLEND),i.disable(i.CULL_FACE),i.disable(i.DEPTH_TEST),i.disable(i.POLYGON_OFFSET_FILL),i.disable(i.SCISSOR_TEST),i.disable(i.STENCIL_TEST),i.disable(i.SAMPLE_ALPHA_TO_COVERAGE),i.blendEquation(i.FUNC_ADD),i.blendFunc(i.ONE,i.ZERO),i.blendFuncSeparate(i.ONE,i.ZERO,i.ONE,i.ZERO),i.blendColor(0,0,0,0),i.colorMask(!0,!0,!0,!0),i.clearColor(0,0,0,0),i.depthMask(!0),i.depthFunc(i.LESS),l.setReversed(!1),i.clearDepth(1),i.stencilMask(4294967295),i.stencilFunc(i.ALWAYS,0,4294967295),i.stencilOp(i.KEEP,i.KEEP,i.KEEP),i.clearStencil(0),i.cullFace(i.BACK),i.frontFace(i.CCW),i.polygonOffset(0,0),i.activeTexture(i.TEXTURE0),i.bindFramebuffer(i.FRAMEBUFFER,null),i.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),i.bindFramebuffer(i.READ_FRAMEBUFFER,null),i.useProgram(null),i.lineWidth(1),i.scissor(0,0,i.canvas.width,i.canvas.height),i.viewport(0,0,i.canvas.width,i.canvas.height),i.pixelStorei(i.PACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,!1),i.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,!1),i.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,i.BROWSER_DEFAULT_WEBGL),i.pixelStorei(i.PACK_ROW_LENGTH,0),i.pixelStorei(i.PACK_SKIP_PIXELS,0),i.pixelStorei(i.PACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_ROW_LENGTH,0),i.pixelStorei(i.UNPACK_IMAGE_HEIGHT,0),i.pixelStorei(i.UNPACK_SKIP_PIXELS,0),i.pixelStorei(i.UNPACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_SKIP_IMAGES,0),g={},y={},V=null,ge={},m={},S=new WeakMap,T=[],P=null,b=!1,_=null,U=null,z=null,R=null,I=null,L=null,B=null,w=new ht(0,0,0),D=0,O=!1,q=null,Y=null,J=null,H=null,te=null,Ut.set(0,0,i.canvas.width,i.canvas.height),mt.set(0,0,i.canvas.width,i.canvas.height),o.reset(),l.reset(),h.reset()}return{buffers:{color:o,depth:l,stencil:h},enable:fe,disable:ke,bindFramebuffer:st,drawBuffers:Be,useProgram:ut,setBlending:gt,setMaterial:rt,setFlipSided:tt,setCullFace:St,setLineWidth:Bt,setPolygonOffset:Ie,setScissorTest:Ue,activeTexture:Vt,bindTexture:W,unbindTexture:Dt,compressedTexImage2D:Ct,compressedTexImage3D:F,texImage2D:re,texImage3D:he,pixelStorei:Xe,getParameter:Ce,updateUBOMapping:He,uniformBlockBinding:Je,texStorage2D:Ee,texStorage3D:Ae,texSubImage2D:x,texSubImage3D:Z,compressedTexSubImage2D:ne,compressedTexSubImage3D:oe,scissor:xe,viewport:Te,reset:ot}}function Pb(i,e,t,n,s,o,l){let h=e.has("WEBGL_multisampled_render_to_texture")?e.get("WEBGL_multisampled_render_to_texture"):null,d=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),f=new nt,g=new WeakMap,y=new Set,m,S=new WeakMap,T=!1;try{T=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function P(F,x){return T?new OffscreenCanvas(F,x):fs("canvas")}function b(F,x,Z){let ne=1,oe=Ct(F);if((oe.width>Z||oe.height>Z)&&(ne=Z/Math.max(oe.width,oe.height)),ne<1)if(typeof HTMLImageElement<"u"&&F instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&F instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&F instanceof ImageBitmap||typeof VideoFrame<"u"&&F instanceof VideoFrame){let Ee=Math.floor(ne*oe.width),Ae=Math.floor(ne*oe.height);m===void 0&&(m=P(Ee,Ae));let re=x?P(Ee,Ae):m;return re.width=Ee,re.height=Ae,re.getContext("2d").drawImage(F,0,0,Ee,Ae),et("WebGLRenderer: Texture has been resized from ("+oe.width+"x"+oe.height+") to ("+Ee+"x"+Ae+")."),re}else return"data"in F&&et("WebGLRenderer: Image in DataTexture is too big ("+oe.width+"x"+oe.height+")."),F;return F}function _(F){return F.generateMipmaps}function U(F){i.generateMipmap(F)}function z(F){return F.isWebGLCubeRenderTarget?i.TEXTURE_CUBE_MAP:F.isWebGL3DRenderTarget?i.TEXTURE_3D:F.isWebGLArrayRenderTarget||F.isCompressedArrayTexture?i.TEXTURE_2D_ARRAY:i.TEXTURE_2D}function R(F,x,Z,ne,oe,Ee=!1){if(F!==null){if(i[F]!==void 0)return i[F];et("WebGLRenderer: Attempt to use non-existing WebGL internal format '"+F+"'")}let Ae;ne&&(Ae=e.get("EXT_texture_norm16"),Ae||et("WebGLRenderer: Unable to use normalized textures without EXT_texture_norm16 extension"));let re=x;if(x===i.RED&&(Z===i.FLOAT&&(re=i.R32F),Z===i.HALF_FLOAT&&(re=i.R16F),Z===i.UNSIGNED_BYTE&&(re=i.R8),Z===i.UNSIGNED_SHORT&&Ae&&(re=Ae.R16_EXT),Z===i.SHORT&&Ae&&(re=Ae.R16_SNORM_EXT)),x===i.RED_INTEGER&&(Z===i.UNSIGNED_BYTE&&(re=i.R8UI),Z===i.UNSIGNED_SHORT&&(re=i.R16UI),Z===i.UNSIGNED_INT&&(re=i.R32UI),Z===i.BYTE&&(re=i.R8I),Z===i.SHORT&&(re=i.R16I),Z===i.INT&&(re=i.R32I)),x===i.RG&&(Z===i.FLOAT&&(re=i.RG32F),Z===i.HALF_FLOAT&&(re=i.RG16F),Z===i.UNSIGNED_BYTE&&(re=i.RG8),Z===i.UNSIGNED_SHORT&&Ae&&(re=Ae.RG16_EXT),Z===i.SHORT&&Ae&&(re=Ae.RG16_SNORM_EXT)),x===i.RG_INTEGER&&(Z===i.UNSIGNED_BYTE&&(re=i.RG8UI),Z===i.UNSIGNED_SHORT&&(re=i.RG16UI),Z===i.UNSIGNED_INT&&(re=i.RG32UI),Z===i.BYTE&&(re=i.RG8I),Z===i.SHORT&&(re=i.RG16I),Z===i.INT&&(re=i.RG32I)),x===i.RGB_INTEGER&&(Z===i.UNSIGNED_BYTE&&(re=i.RGB8UI),Z===i.UNSIGNED_SHORT&&(re=i.RGB16UI),Z===i.UNSIGNED_INT&&(re=i.RGB32UI),Z===i.BYTE&&(re=i.RGB8I),Z===i.SHORT&&(re=i.RGB16I),Z===i.INT&&(re=i.RGB32I)),x===i.RGBA_INTEGER&&(Z===i.UNSIGNED_BYTE&&(re=i.RGBA8UI),Z===i.UNSIGNED_SHORT&&(re=i.RGBA16UI),Z===i.UNSIGNED_INT&&(re=i.RGBA32UI),Z===i.BYTE&&(re=i.RGBA8I),Z===i.SHORT&&(re=i.RGBA16I),Z===i.INT&&(re=i.RGBA32I)),x===i.RGB&&(Z===i.UNSIGNED_SHORT&&Ae&&(re=Ae.RGB16_EXT),Z===i.SHORT&&Ae&&(re=Ae.RGB16_SNORM_EXT),Z===i.UNSIGNED_INT_5_9_9_9_REV&&(re=i.RGB9_E5),Z===i.UNSIGNED_INT_10F_11F_11F_REV&&(re=i.R11F_G11F_B10F)),x===i.RGBA){let he=Ee?ds:xt.getTransfer(oe);Z===i.FLOAT&&(re=i.RGBA32F),Z===i.HALF_FLOAT&&(re=i.RGBA16F),Z===i.UNSIGNED_BYTE&&(re=he===It?i.SRGB8_ALPHA8:i.RGBA8),Z===i.UNSIGNED_SHORT&&Ae&&(re=Ae.RGBA16_EXT),Z===i.SHORT&&Ae&&(re=Ae.RGBA16_SNORM_EXT),Z===i.UNSIGNED_SHORT_4_4_4_4&&(re=i.RGBA4),Z===i.UNSIGNED_SHORT_5_5_5_1&&(re=i.RGB5_A1)}return(re===i.R16F||re===i.R32F||re===i.RG16F||re===i.RG32F||re===i.RGBA16F||re===i.RGBA32F)&&e.get("EXT_color_buffer_float"),re}function I(F,x){let Z;return F?x===null||x===Kn||x===$r?Z=i.DEPTH24_STENCIL8:x===Qn?Z=i.DEPTH32F_STENCIL8:x===Xr&&(Z=i.DEPTH24_STENCIL8,et("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):x===null||x===Kn||x===$r?Z=i.DEPTH_COMPONENT24:x===Qn?Z=i.DEPTH_COMPONENT32F:x===Xr&&(Z=i.DEPTH_COMPONENT16),Z}function L(F,x){return _(F)===!0||F.isFramebufferTexture&&F.minFilter!==an&&F.minFilter!==ln?Math.log2(Math.max(x.width,x.height))+1:F.mipmaps!==void 0&&F.mipmaps.length>0?F.mipmaps.length:F.isCompressedTexture&&Array.isArray(F.image)?x.mipmaps.length:1}function B(F){let x=F.target;x.removeEventListener("dispose",B),D(x),x.isVideoTexture&&g.delete(x),x.isHTMLTexture&&y.delete(x)}function w(F){let x=F.target;x.removeEventListener("dispose",w),q(x)}function D(F){let x=n.get(F);if(x.__webglInit===void 0)return;let Z=F.source,ne=S.get(Z);if(ne){let oe=ne[x.__cacheKey];oe.usedTimes--,oe.usedTimes===0&&O(F),Object.keys(ne).length===0&&S.delete(Z)}n.remove(F)}function O(F){let x=n.get(F);i.deleteTexture(x.__webglTexture);let Z=F.source,ne=S.get(Z);delete ne[x.__cacheKey],l.memory.textures--}function q(F){let x=n.get(F);if(F.depthTexture&&(F.depthTexture.dispose(),n.remove(F.depthTexture)),F.isWebGLCubeRenderTarget)for(let ne=0;ne<6;ne++){if(Array.isArray(x.__webglFramebuffer[ne]))for(let oe=0;oe<x.__webglFramebuffer[ne].length;oe++)i.deleteFramebuffer(x.__webglFramebuffer[ne][oe]);else i.deleteFramebuffer(x.__webglFramebuffer[ne]);x.__webglDepthbuffer&&i.deleteRenderbuffer(x.__webglDepthbuffer[ne])}else{if(Array.isArray(x.__webglFramebuffer))for(let ne=0;ne<x.__webglFramebuffer.length;ne++)i.deleteFramebuffer(x.__webglFramebuffer[ne]);else i.deleteFramebuffer(x.__webglFramebuffer);if(x.__webglDepthbuffer&&i.deleteRenderbuffer(x.__webglDepthbuffer),x.__webglMultisampledFramebuffer&&i.deleteFramebuffer(x.__webglMultisampledFramebuffer),x.__webglColorRenderbuffer)for(let ne=0;ne<x.__webglColorRenderbuffer.length;ne++)x.__webglColorRenderbuffer[ne]&&i.deleteRenderbuffer(x.__webglColorRenderbuffer[ne]);x.__webglDepthRenderbuffer&&i.deleteRenderbuffer(x.__webglDepthRenderbuffer)}let Z=F.textures;for(let ne=0,oe=Z.length;ne<oe;ne++){let Ee=n.get(Z[ne]);Ee.__webglTexture&&(i.deleteTexture(Ee.__webglTexture),l.memory.textures--),n.remove(Z[ne])}n.remove(F)}let Y=0;function J(){Y=0}function H(){return Y}function te(F){Y=F}function k(){let F=Y;return F>=s.maxTextures&&et("WebGLTextures: Trying to use "+(F+1)+" texture units while this GPU supports only "+s.maxTextures),Y+=1,F}function se(F){let x=[];return x.push(F.wrapS),x.push(F.wrapT),x.push(F.wrapR||0),x.push(F.magFilter),x.push(F.minFilter),x.push(F.anisotropy),x.push(F.internalFormat),x.push(F.format),x.push(F.type),x.push(F.generateMipmaps),x.push(F.premultiplyAlpha),x.push(F.flipY),x.push(F.unpackAlignment),x.push(F.colorSpace),x.join()}function _e(F,x){let Z=n.get(F);if(F.isVideoTexture&&W(F),F.isRenderTargetTexture===!1&&F.isExternalTexture!==!0&&F.version>0&&Z.__version!==F.version){let ne=F.image;if(ne===null)et("WebGLRenderer: Texture marked for update but no image data found.");else if(ne.complete===!1)et("WebGLRenderer: Texture marked for update but image is incomplete");else{ke(Z,F,x);return}}else F.isExternalTexture&&(Z.__webglTexture=F.sourceTexture?F.sourceTexture:null);t.bindTexture(i.TEXTURE_2D,Z.__webglTexture,i.TEXTURE0+x)}function ae(F,x){let Z=n.get(F);if(F.isRenderTargetTexture===!1&&F.version>0&&Z.__version!==F.version){ke(Z,F,x);return}else F.isExternalTexture&&(Z.__webglTexture=F.sourceTexture?F.sourceTexture:null);t.bindTexture(i.TEXTURE_2D_ARRAY,Z.__webglTexture,i.TEXTURE0+x)}function V(F,x){let Z=n.get(F);if(F.isRenderTargetTexture===!1&&F.version>0&&Z.__version!==F.version){ke(Z,F,x);return}t.bindTexture(i.TEXTURE_3D,Z.__webglTexture,i.TEXTURE0+x)}function ge(F,x){let Z=n.get(F);if(F.isCubeDepthTexture!==!0&&F.version>0&&Z.__version!==F.version){st(Z,F,x);return}t.bindTexture(i.TEXTURE_CUBE_MAP,Z.__webglTexture,i.TEXTURE0+x)}let Ye={[Ha]:i.REPEAT,[si]:i.CLAMP_TO_EDGE,[Wa]:i.MIRRORED_REPEAT},$e={[an]:i.NEAREST,[Gu]:i.NEAREST_MIPMAP_NEAREST,[Fs]:i.NEAREST_MIPMAP_LINEAR,[ln]:i.LINEAR,[So]:i.LINEAR_MIPMAP_NEAREST,[Vi]:i.LINEAR_MIPMAP_LINEAR},Ut={[$u]:i.NEVER,[Ju]:i.ALWAYS,[ju]:i.LESS,[sl]:i.LEQUAL,[qu]:i.EQUAL,[al]:i.GEQUAL,[Yu]:i.GREATER,[Zu]:i.NOTEQUAL};function mt(F,x){if(x.type===Qn&&e.has("OES_texture_float_linear")===!1&&(x.magFilter===ln||x.magFilter===So||x.magFilter===Fs||x.magFilter===Vi||x.minFilter===ln||x.minFilter===So||x.minFilter===Fs||x.minFilter===Vi)&&et("WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),i.texParameteri(F,i.TEXTURE_WRAP_S,Ye[x.wrapS]),i.texParameteri(F,i.TEXTURE_WRAP_T,Ye[x.wrapT]),(F===i.TEXTURE_3D||F===i.TEXTURE_2D_ARRAY)&&i.texParameteri(F,i.TEXTURE_WRAP_R,Ye[x.wrapR]),i.texParameteri(F,i.TEXTURE_MAG_FILTER,$e[x.magFilter]),i.texParameteri(F,i.TEXTURE_MIN_FILTER,$e[x.minFilter]),x.compareFunction&&(i.texParameteri(F,i.TEXTURE_COMPARE_MODE,i.COMPARE_REF_TO_TEXTURE),i.texParameteri(F,i.TEXTURE_COMPARE_FUNC,Ut[x.compareFunction])),e.has("EXT_texture_filter_anisotropic")===!0){if(x.magFilter===an||x.minFilter!==Fs&&x.minFilter!==Vi||x.type===Qn&&e.has("OES_texture_float_linear")===!1)return;if(x.anisotropy>1||n.get(x).__currentAnisotropy){let Z=e.get("EXT_texture_filter_anisotropic");i.texParameterf(F,Z.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(x.anisotropy,s.getMaxAnisotropy())),n.get(x).__currentAnisotropy=x.anisotropy}}}function Ke(F,x){let Z=!1;F.__webglInit===void 0&&(F.__webglInit=!0,x.addEventListener("dispose",B));let ne=x.source,oe=S.get(ne);oe===void 0&&(oe={},S.set(ne,oe));let Ee=se(x);if(Ee!==F.__cacheKey){oe[Ee]===void 0&&(oe[Ee]={texture:i.createTexture(),usedTimes:0},l.memory.textures++,Z=!0),oe[Ee].usedTimes++;let Ae=oe[F.__cacheKey];Ae!==void 0&&(oe[F.__cacheKey].usedTimes--,Ae.usedTimes===0&&O(x)),F.__cacheKey=Ee,F.__webglTexture=oe[Ee].texture}return Z}function le(F,x,Z){return Math.floor(Math.floor(F/Z)/x)}function fe(F,x,Z,ne){let Ee=F.updateRanges;if(Ee.length===0)t.texSubImage2D(i.TEXTURE_2D,0,0,0,x.width,x.height,Z,ne,x.data);else{Ee.sort((Xe,xe)=>Xe.start-xe.start);let Ae=0;for(let Xe=1;Xe<Ee.length;Xe++){let xe=Ee[Ae],Te=Ee[Xe],He=xe.start+xe.count,Je=le(Te.start,x.width,4),ot=le(xe.start,x.width,4);Te.start<=He+1&&Je===ot&&le(Te.start+Te.count-1,x.width,4)===Je?xe.count=Math.max(xe.count,Te.start+Te.count-xe.start):(++Ae,Ee[Ae]=Te)}Ee.length=Ae+1;let re=t.getParameter(i.UNPACK_ROW_LENGTH),he=t.getParameter(i.UNPACK_SKIP_PIXELS),Ce=t.getParameter(i.UNPACK_SKIP_ROWS);t.pixelStorei(i.UNPACK_ROW_LENGTH,x.width);for(let Xe=0,xe=Ee.length;Xe<xe;Xe++){let Te=Ee[Xe],He=Math.floor(Te.start/4),Je=Math.ceil(Te.count/4),ot=He%x.width,X=Math.floor(He/x.width),Re=Je,de=1;t.pixelStorei(i.UNPACK_SKIP_PIXELS,ot),t.pixelStorei(i.UNPACK_SKIP_ROWS,X),t.texSubImage2D(i.TEXTURE_2D,0,ot,X,Re,de,Z,ne,x.data)}F.clearUpdateRanges(),t.pixelStorei(i.UNPACK_ROW_LENGTH,re),t.pixelStorei(i.UNPACK_SKIP_PIXELS,he),t.pixelStorei(i.UNPACK_SKIP_ROWS,Ce)}}function ke(F,x,Z){let ne=i.TEXTURE_2D;(x.isDataArrayTexture||x.isCompressedArrayTexture)&&(ne=i.TEXTURE_2D_ARRAY),x.isData3DTexture&&(ne=i.TEXTURE_3D);let oe=Ke(F,x),Ee=x.source;t.bindTexture(ne,F.__webglTexture,i.TEXTURE0+Z);let Ae=n.get(Ee);if(Ee.version!==Ae.__version||oe===!0){if(t.activeTexture(i.TEXTURE0+Z),(typeof ImageBitmap<"u"&&x.image instanceof ImageBitmap)===!1){let de=xt.getPrimaries(xt.workingColorSpace),Pe=x.colorSpace===bi?null:xt.getPrimaries(x.colorSpace),Ne=x.colorSpace===bi||de===Pe?i.NONE:i.BROWSER_DEFAULT_WEBGL;t.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,x.flipY),t.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,x.premultiplyAlpha),t.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,Ne)}t.pixelStorei(i.UNPACK_ALIGNMENT,x.unpackAlignment);let he=b(x.image,!1,s.maxTextureSize);he=Dt(x,he);let Ce=o.convert(x.format,x.colorSpace),Xe=o.convert(x.type),xe=R(x.internalFormat,Ce,Xe,x.normalized,x.colorSpace,x.isVideoTexture);mt(ne,x);let Te,He=x.mipmaps,Je=x.isVideoTexture!==!0,ot=Ae.__version===void 0||oe===!0,X=Ee.dataReady,Re=L(x,he);if(x.isDepthTexture)xe=I(x.format===Gi,x.type),ot&&(Je?t.texStorage2D(i.TEXTURE_2D,1,xe,he.width,he.height):t.texImage2D(i.TEXTURE_2D,0,xe,he.width,he.height,0,Ce,Xe,null));else if(x.isDataTexture)if(He.length>0){Je&&ot&&t.texStorage2D(i.TEXTURE_2D,Re,xe,He[0].width,He[0].height);for(let de=0,Pe=He.length;de<Pe;de++)Te=He[de],Je?X&&t.texSubImage2D(i.TEXTURE_2D,de,0,0,Te.width,Te.height,Ce,Xe,Te.data):t.texImage2D(i.TEXTURE_2D,de,xe,Te.width,Te.height,0,Ce,Xe,Te.data);x.generateMipmaps=!1}else Je?(ot&&t.texStorage2D(i.TEXTURE_2D,Re,xe,he.width,he.height),X&&fe(x,he,Ce,Xe)):t.texImage2D(i.TEXTURE_2D,0,xe,he.width,he.height,0,Ce,Xe,he.data);else if(x.isCompressedTexture)if(x.isCompressedArrayTexture){Je&&ot&&t.texStorage3D(i.TEXTURE_2D_ARRAY,Re,xe,He[0].width,He[0].height,he.depth);for(let de=0,Pe=He.length;de<Pe;de++)if(Te=He[de],x.format!==kn)if(Ce!==null)if(Je){if(X)if(x.layerUpdates.size>0){let Ne=Bc(Te.width,Te.height,x.format,x.type);for(let me of x.layerUpdates){let je=Te.data.subarray(me*Ne/Te.data.BYTES_PER_ELEMENT,(me+1)*Ne/Te.data.BYTES_PER_ELEMENT);t.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,de,0,0,me,Te.width,Te.height,1,Ce,je)}}else t.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,de,0,0,0,Te.width,Te.height,he.depth,Ce,Te.data)}else t.compressedTexImage3D(i.TEXTURE_2D_ARRAY,de,xe,Te.width,Te.height,he.depth,0,Te.data,0,0);else et("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else Je?X&&t.texSubImage3D(i.TEXTURE_2D_ARRAY,de,0,0,0,Te.width,Te.height,he.depth,Ce,Xe,Te.data):t.texImage3D(i.TEXTURE_2D_ARRAY,de,xe,Te.width,Te.height,he.depth,0,Ce,Xe,Te.data);x.layerUpdates.size>0&&x.clearLayerUpdates()}else{Je&&ot&&t.texStorage2D(i.TEXTURE_2D,Re,xe,He[0].width,He[0].height);for(let de=0,Pe=He.length;de<Pe;de++)Te=He[de],x.format!==kn?Ce!==null?Je?X&&t.compressedTexSubImage2D(i.TEXTURE_2D,de,0,0,Te.width,Te.height,Ce,Te.data):t.compressedTexImage2D(i.TEXTURE_2D,de,xe,Te.width,Te.height,0,Te.data):et("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):Je?X&&t.texSubImage2D(i.TEXTURE_2D,de,0,0,Te.width,Te.height,Ce,Xe,Te.data):t.texImage2D(i.TEXTURE_2D,de,xe,Te.width,Te.height,0,Ce,Xe,Te.data)}else if(x.isDataArrayTexture)if(Je){if(ot&&t.texStorage3D(i.TEXTURE_2D_ARRAY,Re,xe,he.width,he.height,he.depth),X)if(x.layerUpdates.size>0){let de=Bc(he.width,he.height,x.format,x.type);for(let Pe of x.layerUpdates){let Ne=he.data.subarray(Pe*de/he.data.BYTES_PER_ELEMENT,(Pe+1)*de/he.data.BYTES_PER_ELEMENT);t.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,Pe,he.width,he.height,1,Ce,Xe,Ne)}x.clearLayerUpdates()}else t.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,0,he.width,he.height,he.depth,Ce,Xe,he.data)}else t.texImage3D(i.TEXTURE_2D_ARRAY,0,xe,he.width,he.height,he.depth,0,Ce,Xe,he.data);else if(x.isData3DTexture)Je?(ot&&t.texStorage3D(i.TEXTURE_3D,Re,xe,he.width,he.height,he.depth),X&&t.texSubImage3D(i.TEXTURE_3D,0,0,0,0,he.width,he.height,he.depth,Ce,Xe,he.data)):t.texImage3D(i.TEXTURE_3D,0,xe,he.width,he.height,he.depth,0,Ce,Xe,he.data);else if(x.isFramebufferTexture){if(ot)if(Je)t.texStorage2D(i.TEXTURE_2D,Re,xe,he.width,he.height);else{let de=he.width,Pe=he.height;for(let Ne=0;Ne<Re;Ne++)t.texImage2D(i.TEXTURE_2D,Ne,xe,de,Pe,0,Ce,Xe,null),de>>=1,Pe>>=1}}else if(x.isHTMLTexture){if("texElementImage2D"in i){let de=i.canvas;if(de.hasAttribute("layoutsubtree")||de.setAttribute("layoutsubtree","true"),he.parentNode!==de){de.appendChild(he),y.add(x),de.onpaint=Pe=>{let Ne=Pe.changedElements;for(let me of y)Ne.includes(me.image)&&(me.needsUpdate=!0)},de.requestPaint();return}if(i.texElementImage2D.length===3)i.texElementImage2D(i.TEXTURE_2D,i.RGBA8,he);else{let Ne=i.RGBA,me=i.RGBA,je=i.UNSIGNED_BYTE;i.texElementImage2D(i.TEXTURE_2D,0,Ne,me,je,he)}i.texParameteri(i.TEXTURE_2D,i.TEXTURE_MIN_FILTER,i.LINEAR),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_S,i.CLAMP_TO_EDGE),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_T,i.CLAMP_TO_EDGE)}}else if(He.length>0){if(Je&&ot){let de=Ct(He[0]);t.texStorage2D(i.TEXTURE_2D,Re,xe,de.width,de.height)}for(let de=0,Pe=He.length;de<Pe;de++)Te=He[de],Je?X&&t.texSubImage2D(i.TEXTURE_2D,de,0,0,Ce,Xe,Te):t.texImage2D(i.TEXTURE_2D,de,xe,Ce,Xe,Te);x.generateMipmaps=!1}else if(Je){if(ot){let de=Ct(he);t.texStorage2D(i.TEXTURE_2D,Re,xe,de.width,de.height)}X&&t.texSubImage2D(i.TEXTURE_2D,0,0,0,Ce,Xe,he)}else t.texImage2D(i.TEXTURE_2D,0,xe,Ce,Xe,he);_(x)&&U(ne),Ae.__version=Ee.version,x.onUpdate&&x.onUpdate(x)}F.__version=x.version}function st(F,x,Z){if(x.image.length!==6)return;let ne=Ke(F,x),oe=x.source;t.bindTexture(i.TEXTURE_CUBE_MAP,F.__webglTexture,i.TEXTURE0+Z);let Ee=n.get(oe);if(oe.version!==Ee.__version||ne===!0){t.activeTexture(i.TEXTURE0+Z);let Ae=xt.getPrimaries(xt.workingColorSpace),re=x.colorSpace===bi?null:xt.getPrimaries(x.colorSpace),he=x.colorSpace===bi||Ae===re?i.NONE:i.BROWSER_DEFAULT_WEBGL;t.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,x.flipY),t.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,x.premultiplyAlpha),t.pixelStorei(i.UNPACK_ALIGNMENT,x.unpackAlignment),t.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,he);let Ce=x.isCompressedTexture||x.image[0].isCompressedTexture,Xe=x.image[0]&&x.image[0].isDataTexture,xe=[];for(let me=0;me<6;me++)!Ce&&!Xe?xe[me]=b(x.image[me],!0,s.maxCubemapSize):xe[me]=Xe?x.image[me].image:x.image[me],xe[me]=Dt(x,xe[me]);let Te=xe[0],He=o.convert(x.format,x.colorSpace),Je=o.convert(x.type),ot=R(x.internalFormat,He,Je,x.normalized,x.colorSpace),X=x.isVideoTexture!==!0,Re=Ee.__version===void 0||ne===!0,de=oe.dataReady,Pe=L(x,Te);mt(i.TEXTURE_CUBE_MAP,x);let Ne;if(Ce){X&&Re&&t.texStorage2D(i.TEXTURE_CUBE_MAP,Pe,ot,Te.width,Te.height);for(let me=0;me<6;me++){Ne=xe[me].mipmaps;for(let je=0;je<Ne.length;je++){let We=Ne[je];x.format!==kn?He!==null?X?de&&t.compressedTexSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je,0,0,We.width,We.height,He,We.data):t.compressedTexImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je,ot,We.width,We.height,0,We.data):et("WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):X?de&&t.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je,0,0,We.width,We.height,He,Je,We.data):t.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je,ot,We.width,We.height,0,He,Je,We.data)}}}else{if(Ne=x.mipmaps,X&&Re){Ne.length>0&&Pe++;let me=Ct(xe[0]);t.texStorage2D(i.TEXTURE_CUBE_MAP,Pe,ot,me.width,me.height)}for(let me=0;me<6;me++)if(Xe){X?de&&t.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,0,0,0,xe[me].width,xe[me].height,He,Je,xe[me].data):t.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,0,ot,xe[me].width,xe[me].height,0,He,Je,xe[me].data);for(let je=0;je<Ne.length;je++){let Ft=Ne[je].image[me].image;X?de&&t.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je+1,0,0,Ft.width,Ft.height,He,Je,Ft.data):t.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je+1,ot,Ft.width,Ft.height,0,He,Je,Ft.data)}}else{X?de&&t.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,0,0,0,He,Je,xe[me]):t.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,0,ot,He,Je,xe[me]);for(let je=0;je<Ne.length;je++){let We=Ne[je];X?de&&t.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je+1,0,0,He,Je,We.image[me]):t.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+me,je+1,ot,He,Je,We.image[me])}}}_(x)&&U(i.TEXTURE_CUBE_MAP),Ee.__version=oe.version,x.onUpdate&&x.onUpdate(x)}F.__version=x.version}function Be(F,x,Z,ne,oe,Ee){let Ae=o.convert(Z.format,Z.colorSpace),re=o.convert(Z.type),he=R(Z.internalFormat,Ae,re,Z.normalized,Z.colorSpace),Ce=n.get(x),Xe=n.get(Z);if(Xe.__renderTarget=x,!Ce.__hasExternalTextures){let xe=Math.max(1,x.width>>Ee),Te=Math.max(1,x.height>>Ee);oe===i.TEXTURE_3D||oe===i.TEXTURE_2D_ARRAY?t.texImage3D(oe,Ee,he,xe,Te,x.depth,0,Ae,re,null):t.texImage2D(oe,Ee,he,xe,Te,0,Ae,re,null)}t.bindFramebuffer(i.FRAMEBUFFER,F),Vt(x)?h.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,ne,oe,Xe.__webglTexture,0,Ue(x)):(oe===i.TEXTURE_2D||oe>=i.TEXTURE_CUBE_MAP_POSITIVE_X&&oe<=i.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&i.framebufferTexture2D(i.FRAMEBUFFER,ne,oe,Xe.__webglTexture,Ee),t.bindFramebuffer(i.FRAMEBUFFER,null)}function ut(F,x,Z){if(i.bindRenderbuffer(i.RENDERBUFFER,F),x.depthBuffer){let ne=x.depthTexture,oe=ne&&ne.isDepthTexture?ne.type:null,Ee=I(x.stencilBuffer,oe),Ae=x.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;Vt(x)?h.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Ue(x),Ee,x.width,x.height):Z?i.renderbufferStorageMultisample(i.RENDERBUFFER,Ue(x),Ee,x.width,x.height):i.renderbufferStorage(i.RENDERBUFFER,Ee,x.width,x.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,Ae,i.RENDERBUFFER,F)}else{let ne=x.textures;for(let oe=0;oe<ne.length;oe++){let Ee=ne[oe],Ae=o.convert(Ee.format,Ee.colorSpace),re=o.convert(Ee.type),he=R(Ee.internalFormat,Ae,re,Ee.normalized,Ee.colorSpace);Vt(x)?h.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Ue(x),he,x.width,x.height):Z?i.renderbufferStorageMultisample(i.RENDERBUFFER,Ue(x),he,x.width,x.height):i.renderbufferStorage(i.RENDERBUFFER,he,x.width,x.height)}}i.bindRenderbuffer(i.RENDERBUFFER,null)}function $t(F,x,Z){let ne=x.isWebGLCubeRenderTarget===!0;if(t.bindFramebuffer(i.FRAMEBUFFER,F),!(x.depthTexture&&x.depthTexture.isDepthTexture))throw new Error("THREE.WebGLTextures: renderTarget.depthTexture must be an instance of THREE.DepthTexture.");let oe=n.get(x.depthTexture);if(oe.__renderTarget=x,(!oe.__webglTexture||x.depthTexture.image.width!==x.width||x.depthTexture.image.height!==x.height)&&(x.depthTexture.image.width=x.width,x.depthTexture.image.height=x.height,x.depthTexture.needsUpdate=!0),ne){if(oe.__webglInit===void 0&&(oe.__webglInit=!0,x.depthTexture.addEventListener("dispose",B)),oe.__webglTexture===void 0){oe.__webglTexture=i.createTexture(),t.bindTexture(i.TEXTURE_CUBE_MAP,oe.__webglTexture),mt(i.TEXTURE_CUBE_MAP,x.depthTexture);let Ce=o.convert(x.depthTexture.format),Xe=o.convert(x.depthTexture.type),xe;x.depthTexture.format===ai?xe=i.DEPTH_COMPONENT24:x.depthTexture.format===Gi&&(xe=i.DEPTH24_STENCIL8);for(let Te=0;Te<6;Te++)i.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+Te,0,xe,x.width,x.height,0,Ce,Xe,null)}}else _e(x.depthTexture,0);let Ee=oe.__webglTexture,Ae=Ue(x),re=ne?i.TEXTURE_CUBE_MAP_POSITIVE_X+Z:i.TEXTURE_2D,he=x.depthTexture.format===Gi?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;if(x.depthTexture.format===ai)Vt(x)?h.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,he,re,Ee,0,Ae):i.framebufferTexture2D(i.FRAMEBUFFER,he,re,Ee,0);else if(x.depthTexture.format===Gi)Vt(x)?h.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,he,re,Ee,0,Ae):i.framebufferTexture2D(i.FRAMEBUFFER,he,re,Ee,0);else throw new Error("THREE.WebGLTextures: Unknown depthTexture format.")}function dt(F){let x=n.get(F),Z=F.isWebGLCubeRenderTarget===!0;if(x.__boundDepthTexture!==F.depthTexture){let ne=F.depthTexture;if(x.__depthDisposeCallback&&x.__depthDisposeCallback(),ne){let oe=()=>{delete x.__boundDepthTexture,delete x.__depthDisposeCallback,ne.removeEventListener("dispose",oe)};ne.addEventListener("dispose",oe),x.__depthDisposeCallback=oe}x.__boundDepthTexture=ne}if(F.depthTexture&&!x.__autoAllocateDepthBuffer)if(Z)for(let ne=0;ne<6;ne++)$t(x.__webglFramebuffer[ne],F,ne);else{let ne=F.texture.mipmaps;ne&&ne.length>0?$t(x.__webglFramebuffer[0],F,0):$t(x.__webglFramebuffer,F,0)}else if(Z){x.__webglDepthbuffer=[];for(let ne=0;ne<6;ne++)if(t.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer[ne]),x.__webglDepthbuffer[ne]===void 0)x.__webglDepthbuffer[ne]=i.createRenderbuffer(),ut(x.__webglDepthbuffer[ne],F,!1);else{let oe=F.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,Ee=x.__webglDepthbuffer[ne];i.bindRenderbuffer(i.RENDERBUFFER,Ee),i.framebufferRenderbuffer(i.FRAMEBUFFER,oe,i.RENDERBUFFER,Ee)}}else{let ne=F.texture.mipmaps;if(ne&&ne.length>0?t.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer[0]):t.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer),x.__webglDepthbuffer===void 0)x.__webglDepthbuffer=i.createRenderbuffer(),ut(x.__webglDepthbuffer,F,!1);else{let oe=F.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,Ee=x.__webglDepthbuffer;i.bindRenderbuffer(i.RENDERBUFFER,Ee),i.framebufferRenderbuffer(i.FRAMEBUFFER,oe,i.RENDERBUFFER,Ee)}}t.bindFramebuffer(i.FRAMEBUFFER,null)}function gt(F,x,Z){let ne=n.get(F);x!==void 0&&Be(ne.__webglFramebuffer,F,F.texture,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,0),Z!==void 0&&dt(F)}function rt(F){let x=F.texture,Z=n.get(F),ne=n.get(x);F.addEventListener("dispose",w);let oe=F.textures,Ee=F.isWebGLCubeRenderTarget===!0,Ae=oe.length>1;if(Ae||(ne.__webglTexture===void 0&&(ne.__webglTexture=i.createTexture()),ne.__version=x.version,l.memory.textures++),Ee){Z.__webglFramebuffer=[];for(let re=0;re<6;re++)if(x.mipmaps&&x.mipmaps.length>0){Z.__webglFramebuffer[re]=[];for(let he=0;he<x.mipmaps.length;he++)Z.__webglFramebuffer[re][he]=i.createFramebuffer()}else Z.__webglFramebuffer[re]=i.createFramebuffer()}else{if(x.mipmaps&&x.mipmaps.length>0){Z.__webglFramebuffer=[];for(let re=0;re<x.mipmaps.length;re++)Z.__webglFramebuffer[re]=i.createFramebuffer()}else Z.__webglFramebuffer=i.createFramebuffer();if(Ae)for(let re=0,he=oe.length;re<he;re++){let Ce=n.get(oe[re]);Ce.__webglTexture===void 0&&(Ce.__webglTexture=i.createTexture(),l.memory.textures++)}if(F.samples>0&&Vt(F)===!1){Z.__webglMultisampledFramebuffer=i.createFramebuffer(),Z.__webglColorRenderbuffer=[],t.bindFramebuffer(i.FRAMEBUFFER,Z.__webglMultisampledFramebuffer);for(let re=0;re<oe.length;re++){let he=oe[re];Z.__webglColorRenderbuffer[re]=i.createRenderbuffer(),i.bindRenderbuffer(i.RENDERBUFFER,Z.__webglColorRenderbuffer[re]);let Ce=o.convert(he.format,he.colorSpace),Xe=o.convert(he.type),xe=R(he.internalFormat,Ce,Xe,he.normalized,he.colorSpace,F.isXRRenderTarget===!0),Te=Ue(F);i.renderbufferStorageMultisample(i.RENDERBUFFER,Te,xe,F.width,F.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+re,i.RENDERBUFFER,Z.__webglColorRenderbuffer[re])}i.bindRenderbuffer(i.RENDERBUFFER,null),F.depthBuffer&&(Z.__webglDepthRenderbuffer=i.createRenderbuffer(),ut(Z.__webglDepthRenderbuffer,F,!0)),t.bindFramebuffer(i.FRAMEBUFFER,null)}}if(Ee){t.bindTexture(i.TEXTURE_CUBE_MAP,ne.__webglTexture),mt(i.TEXTURE_CUBE_MAP,x);for(let re=0;re<6;re++)if(x.mipmaps&&x.mipmaps.length>0)for(let he=0;he<x.mipmaps.length;he++)Be(Z.__webglFramebuffer[re][he],F,x,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+re,he);else Be(Z.__webglFramebuffer[re],F,x,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+re,0);_(x)&&U(i.TEXTURE_CUBE_MAP),t.unbindTexture()}else if(Ae){for(let re=0,he=oe.length;re<he;re++){let Ce=oe[re],Xe=n.get(Ce),xe=i.TEXTURE_2D;(F.isWebGL3DRenderTarget||F.isWebGLArrayRenderTarget)&&(xe=F.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),t.bindTexture(xe,Xe.__webglTexture),mt(xe,Ce),Be(Z.__webglFramebuffer,F,Ce,i.COLOR_ATTACHMENT0+re,xe,0),_(Ce)&&U(xe)}t.unbindTexture()}else{let re=i.TEXTURE_2D;if((F.isWebGL3DRenderTarget||F.isWebGLArrayRenderTarget)&&(re=F.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),t.bindTexture(re,ne.__webglTexture),mt(re,x),x.mipmaps&&x.mipmaps.length>0)for(let he=0;he<x.mipmaps.length;he++)Be(Z.__webglFramebuffer[he],F,x,i.COLOR_ATTACHMENT0,re,he);else Be(Z.__webglFramebuffer,F,x,i.COLOR_ATTACHMENT0,re,0);_(x)&&U(re),t.unbindTexture()}F.depthBuffer&&dt(F)}function tt(F){let x=F.textures;for(let Z=0,ne=x.length;Z<ne;Z++){let oe=x[Z];if(_(oe)){let Ee=z(F),Ae=n.get(oe).__webglTexture;t.bindTexture(Ee,Ae),U(Ee),t.unbindTexture()}}}let St=[],Bt=[];function Ie(F){if(F.samples>0){if(Vt(F)===!1){let x=F.textures,Z=F.width,ne=F.height,oe=i.COLOR_BUFFER_BIT,Ee=F.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,Ae=n.get(F),re=x.length>1;if(re)for(let Ce=0;Ce<x.length;Ce++)t.bindFramebuffer(i.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+Ce,i.RENDERBUFFER,null),t.bindFramebuffer(i.FRAMEBUFFER,Ae.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+Ce,i.TEXTURE_2D,null,0);t.bindFramebuffer(i.READ_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer);let he=F.texture.mipmaps;he&&he.length>0?t.bindFramebuffer(i.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer[0]):t.bindFramebuffer(i.DRAW_FRAMEBUFFER,Ae.__webglFramebuffer);for(let Ce=0;Ce<x.length;Ce++){if(F.resolveDepthBuffer&&(F.depthBuffer&&(oe|=i.DEPTH_BUFFER_BIT),F.stencilBuffer&&F.resolveStencilBuffer&&(oe|=i.STENCIL_BUFFER_BIT)),re){i.framebufferRenderbuffer(i.READ_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ce]);let Xe=n.get(x[Ce]).__webglTexture;i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,Xe,0)}i.blitFramebuffer(0,0,Z,ne,0,0,Z,ne,oe,i.NEAREST),d===!0&&(St.length=0,Bt.length=0,St.push(i.COLOR_ATTACHMENT0+Ce),F.depthBuffer&&F.storeMultisampledDepthBuffer===!1&&(St.push(Ee),Bt.push(Ee),i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,Bt)),i.invalidateFramebuffer(i.READ_FRAMEBUFFER,St))}if(t.bindFramebuffer(i.READ_FRAMEBUFFER,null),t.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),re)for(let Ce=0;Ce<x.length;Ce++){t.bindFramebuffer(i.FRAMEBUFFER,Ae.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+Ce,i.RENDERBUFFER,Ae.__webglColorRenderbuffer[Ce]);let Xe=n.get(x[Ce]).__webglTexture;t.bindFramebuffer(i.FRAMEBUFFER,Ae.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+Ce,i.TEXTURE_2D,Xe,0)}t.bindFramebuffer(i.DRAW_FRAMEBUFFER,Ae.__webglMultisampledFramebuffer)}else if(F.depthBuffer&&F.storeMultisampledDepthBuffer===!1&&d){let x=F.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,[x])}}}function Ue(F){return Math.min(s.maxSamples,F.samples)}function Vt(F){let x=n.get(F);return F.samples>0&&e.has("WEBGL_multisampled_render_to_texture")===!0&&x.__useRenderToTexture!==!1}function W(F){let x=l.render.frame;g.get(F)!==x&&(g.set(F,x),F.update())}function Dt(F,x){let Z=F.colorSpace,ne=F.format,oe=F.type;return F.isCompressedTexture===!0||F.isVideoTexture===!0||Z!==us&&Z!==bi&&(xt.getTransfer(Z)===It?(ne!==kn||oe!==En)&&et("WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):it("WebGLTextures: Unsupported texture color space:",Z)),x}function Ct(F){return typeof HTMLImageElement<"u"&&F instanceof HTMLImageElement?(f.width=F.naturalWidth||F.width,f.height=F.naturalHeight||F.height):typeof VideoFrame<"u"&&F instanceof VideoFrame?(f.width=F.displayWidth,f.height=F.displayHeight):(f.width=F.width,f.height=F.height),f}this.allocateTextureUnit=k,this.resetTextureUnits=J,this.getTextureUnits=H,this.setTextureUnits=te,this.setTexture2D=_e,this.setTexture2DArray=ae,this.setTexture3D=V,this.setTextureCube=ge,this.rebindTextures=gt,this.setupRenderTarget=rt,this.updateRenderTargetMipmap=tt,this.updateMultisampleRenderTarget=Ie,this.setupDepthRenderbuffer=dt,this.setupFrameBufferTexture=Be,this.useMultisampledRTT=Vt,this.isReversedDepthBuffer=function(){return t.buffers.depth.getReversed()}}function Ib(i,e){function t(n,s=bi){let o,l=xt.getTransfer(s);if(n===En)return i.UNSIGNED_BYTE;if(n===Mo)return i.UNSIGNED_SHORT_4_4_4_4;if(n===Eo)return i.UNSIGNED_SHORT_5_5_5_1;if(n===Tc)return i.UNSIGNED_INT_5_9_9_9_REV;if(n===Ac)return i.UNSIGNED_INT_10F_11F_11F_REV;if(n===Ec)return i.BYTE;if(n===wc)return i.SHORT;if(n===Xr)return i.UNSIGNED_SHORT;if(n===bo)return i.INT;if(n===Kn)return i.UNSIGNED_INT;if(n===Qn)return i.FLOAT;if(n===ei)return i.HALF_FLOAT;if(n===Cc)return i.ALPHA;if(n===Rc)return i.RGB;if(n===kn)return i.RGBA;if(n===ai)return i.DEPTH_COMPONENT;if(n===Gi)return i.DEPTH_STENCIL;if(n===Pc)return i.RED;if(n===wo)return i.RED_INTEGER;if(n===Hi)return i.RG;if(n===To)return i.RG_INTEGER;if(n===Ao)return i.RGBA_INTEGER;if(n===Ns||n===Us||n===Os||n===Bs)if(l===It)if(o=e.get("WEBGL_compressed_texture_s3tc_srgb"),o!==null){if(n===Ns)return o.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(n===Us)return o.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(n===Os)return o.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(n===Bs)return o.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(o=e.get("WEBGL_compressed_texture_s3tc"),o!==null){if(n===Ns)return o.COMPRESSED_RGB_S3TC_DXT1_EXT;if(n===Us)return o.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(n===Os)return o.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(n===Bs)return o.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(n===Co||n===Ro||n===Po||n===Io)if(o=e.get("WEBGL_compressed_texture_pvrtc"),o!==null){if(n===Co)return o.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(n===Ro)return o.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(n===Po)return o.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(n===Io)return o.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(n===Do||n===Lo||n===Fo||n===No||n===Uo||n===ks||n===Oo)if(o=e.get("WEBGL_compressed_texture_etc"),o!==null){if(n===Do||n===Lo)return l===It?o.COMPRESSED_SRGB8_ETC2:o.COMPRESSED_RGB8_ETC2;if(n===Fo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:o.COMPRESSED_RGBA8_ETC2_EAC;if(n===No)return o.COMPRESSED_R11_EAC;if(n===Uo)return o.COMPRESSED_SIGNED_R11_EAC;if(n===ks)return o.COMPRESSED_RG11_EAC;if(n===Oo)return o.COMPRESSED_SIGNED_RG11_EAC}else return null;if(n===Bo||n===ko||n===zo||n===Vo||n===Go||n===Ho||n===Wo||n===Xo||n===$o||n===jo||n===qo||n===Yo||n===Zo||n===Jo)if(o=e.get("WEBGL_compressed_texture_astc"),o!==null){if(n===Bo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:o.COMPRESSED_RGBA_ASTC_4x4_KHR;if(n===ko)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:o.COMPRESSED_RGBA_ASTC_5x4_KHR;if(n===zo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:o.COMPRESSED_RGBA_ASTC_5x5_KHR;if(n===Vo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:o.COMPRESSED_RGBA_ASTC_6x5_KHR;if(n===Go)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:o.COMPRESSED_RGBA_ASTC_6x6_KHR;if(n===Ho)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:o.COMPRESSED_RGBA_ASTC_8x5_KHR;if(n===Wo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:o.COMPRESSED_RGBA_ASTC_8x6_KHR;if(n===Xo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:o.COMPRESSED_RGBA_ASTC_8x8_KHR;if(n===$o)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:o.COMPRESSED_RGBA_ASTC_10x5_KHR;if(n===jo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:o.COMPRESSED_RGBA_ASTC_10x6_KHR;if(n===qo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:o.COMPRESSED_RGBA_ASTC_10x8_KHR;if(n===Yo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:o.COMPRESSED_RGBA_ASTC_10x10_KHR;if(n===Zo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:o.COMPRESSED_RGBA_ASTC_12x10_KHR;if(n===Jo)return l===It?o.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:o.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(n===Ko||n===Qo||n===el)if(o=e.get("EXT_texture_compression_bptc"),o!==null){if(n===Ko)return l===It?o.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:o.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(n===Qo)return o.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(n===el)return o.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(n===tl||n===nl||n===zs||n===il)if(o=e.get("EXT_texture_compression_rgtc"),o!==null){if(n===tl)return o.COMPRESSED_RED_RGTC1_EXT;if(n===nl)return o.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(n===zs)return o.COMPRESSED_RED_GREEN_RGTC2_EXT;if(n===il)return o.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return n===$r?i.UNSIGNED_INT_24_8:i[n]!==void 0?i[n]:null}return{convert:t}}var Db=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,Lb=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`,Kc=class{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(e,t){if(this.texture===null){let n=new xs(e.texture);(e.depthNear!==t.depthNear||e.depthFar!==t.depthFar)&&(this.depthNear=e.depthNear,this.depthFar=e.depthFar),this.texture=n}}getMesh(e){if(this.texture!==null&&this.mesh===null){let t=e.cameras[0].viewport,n=new Dn({vertexShader:Db,fragmentShader:Lb,uniforms:{depthColor:{value:this.texture},depthWidth:{value:t.z},depthHeight:{value:t.w}}});this.mesh=new yn(new sr(20,20),n)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}},Qc=class extends Zn{constructor(e,t){super();let n=this,s=null,o=1,l=null,h="local-floor",d=1,f=null,g=null,y=null,m=null,S=null,T=null,P=typeof XRWebGLBinding<"u",b=new Kc,_={},U=t.getContextAttributes(),z=null,R=null,I=[],L=[],B=new nt,w=null,D=null,O=new fn;O.viewport=new Ht;let q=new fn;q.viewport=new Ht;let Y=[O,q],J=new _o,H=null,te=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(le){let fe=I[le];return fe===void 0&&(fe=new Ur,I[le]=fe),fe.getTargetRaySpace()},this.getControllerGrip=function(le){let fe=I[le];return fe===void 0&&(fe=new Ur,I[le]=fe),fe.getGripSpace()},this.getHand=function(le){let fe=I[le];return fe===void 0&&(fe=new Ur,I[le]=fe),fe.getHandSpace()};function k(le){let fe=L.indexOf(le.inputSource);if(fe===-1)return;let ke=I[fe];ke!==void 0&&(ke.update(le.inputSource,le.frame,f||l),ke.dispatchEvent({type:le.type,data:le.inputSource}))}function se(){s.removeEventListener("select",k),s.removeEventListener("selectstart",k),s.removeEventListener("selectend",k),s.removeEventListener("squeeze",k),s.removeEventListener("squeezestart",k),s.removeEventListener("squeezeend",k),s.removeEventListener("end",se),s.removeEventListener("inputsourceschange",_e);for(let le=0;le<I.length;le++){let fe=L[le];fe!==null&&(L[le]=null,I[le].disconnect(fe))}H=null,te=null,b.reset();for(let le in _)delete _[le];if(e.setRenderTarget(z),S=null,m=null,y=null,s=null,R=null,Ke.stop(),n.isPresenting=!1,e.setPixelRatio(w),e.setSize(B.width,B.height,!1),D!==null){let le=D.camera;le.fov=D.fov,le.zoom=D.zoom,le.updateProjectionMatrix(),D=null}n.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(le){o=le,n.isPresenting===!0&&et("WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(le){h=le,n.isPresenting===!0&&et("WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return f||l},this.setReferenceSpace=function(le){f=le},this.getBaseLayer=function(){return m!==null?m:S},this.getBinding=function(){return y===null&&P&&(y=new XRWebGLBinding(s,t)),y},this.getFrame=function(){return T},this.getSession=function(){return s},this.setSession=async function(le){if(s=le,s!==null){if(z=e.getRenderTarget(),s.addEventListener("select",k),s.addEventListener("selectstart",k),s.addEventListener("selectend",k),s.addEventListener("squeeze",k),s.addEventListener("squeezestart",k),s.addEventListener("squeezeend",k),s.addEventListener("end",se),s.addEventListener("inputsourceschange",_e),U.xrCompatible!==!0&&await t.makeXRCompatible(),w=e.getPixelRatio(),e.getSize(B),P&&"createProjectionLayer"in XRWebGLBinding.prototype){let ke=null,st=null,Be=null;U.depth&&(Be=U.stencil?t.DEPTH24_STENCIL8:t.DEPTH_COMPONENT24,ke=U.stencil?Gi:ai,st=U.stencil?$r:Kn);let ut={colorFormat:t.RGBA8,depthFormat:Be,scaleFactor:o};y=this.getBinding(),m=y.createProjectionLayer(ut),s.updateRenderState({layers:[m]}),e.setPixelRatio(1),e.setSize(m.textureWidth,m.textureHeight,!1),R=new Mn(m.textureWidth,m.textureHeight,{format:kn,type:En,depthTexture:new Li(m.textureWidth,m.textureHeight,st,void 0,void 0,void 0,void 0,void 0,void 0,ke),stencilBuffer:U.stencil,colorSpace:e.outputColorSpace,samples:U.antialias?4:0,resolveDepthBuffer:m.ignoreDepthValues===!1,resolveStencilBuffer:m.ignoreDepthValues===!1,storeMultisampledDepthBuffer:m.ignoreDepthValues===!1,storeMultisampledStencilBuffer:m.ignoreDepthValues===!1})}else{let ke={antialias:U.antialias,alpha:!0,depth:U.depth,stencil:U.stencil,framebufferScaleFactor:o};S=new XRWebGLLayer(s,t,ke),s.updateRenderState({baseLayer:S}),e.setPixelRatio(1),e.setSize(S.framebufferWidth,S.framebufferHeight,!1),R=new Mn(S.framebufferWidth,S.framebufferHeight,{format:kn,type:En,colorSpace:e.outputColorSpace,stencilBuffer:U.stencil,resolveDepthBuffer:S.ignoreDepthValues===!1,resolveStencilBuffer:S.ignoreDepthValues===!1,storeMultisampledDepthBuffer:S.ignoreDepthValues===!1,storeMultisampledStencilBuffer:S.ignoreDepthValues===!1})}R.isXRRenderTarget=!0,this.setFoveation(d),f=null,l=await s.requestReferenceSpace(h),Ke.setContext(s),Ke.start(),n.isPresenting=!0,n.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(s!==null)return s.environmentBlendMode},this.getDepthTexture=function(){return b.getDepthTexture()};function _e(le){for(let fe=0;fe<le.removed.length;fe++){let ke=le.removed[fe],st=L.indexOf(ke);st>=0&&(L[st]=null,I[st].disconnect(ke))}for(let fe=0;fe<le.added.length;fe++){let ke=le.added[fe],st=L.indexOf(ke);if(st===-1){for(let ut=0;ut<I.length;ut++)if(ut>=L.length){L.push(ke),st=ut;break}else if(L[ut]===null){L[ut]=ke,st=ut;break}if(st===-1)break}let Be=I[st];Be&&Be.connect(ke)}}let ae=new j,V=new j;function ge(le,fe,ke){ae.setFromMatrixPosition(fe.matrixWorld),V.setFromMatrixPosition(ke.matrixWorld);let st=ae.distanceTo(V),Be=fe.projectionMatrix.elements,ut=ke.projectionMatrix.elements,$t=Be[14]/(Be[10]-1),dt=Be[14]/(Be[10]+1),gt=(Be[9]+1)/Be[5],rt=(Be[9]-1)/Be[5],tt=(Be[8]-1)/Be[0],St=(ut[8]+1)/ut[0],Bt=$t*tt,Ie=$t*St,Ue=st/(-tt+St),Vt=Ue*-tt;if(fe.matrixWorld.decompose(le.position,le.quaternion,le.scale),le.translateX(Vt),le.translateZ(Ue),le.matrixWorld.compose(le.position,le.quaternion,le.scale),le.matrixWorldInverse.copy(le.matrixWorld).invert(),Be[10]===-1)le.projectionMatrix.copy(fe.projectionMatrix),le.projectionMatrixInverse.copy(fe.projectionMatrixInverse);else{let W=$t+Ue,Dt=dt+Ue,Ct=Bt-Vt,F=Ie+(st-Vt),x=gt*dt/Dt*W,Z=rt*dt/Dt*W;le.projectionMatrix.makePerspective(Ct,F,x,Z,W,Dt),le.projectionMatrixInverse.copy(le.projectionMatrix).invert()}}function Ye(le,fe){fe===null?le.matrixWorld.copy(le.matrix):le.matrixWorld.multiplyMatrices(fe.matrixWorld,le.matrix),le.matrixWorldInverse.copy(le.matrixWorld).invert()}this.updateCamera=function(le){if(s===null)return;let fe=le.near,ke=le.far;b.texture!==null&&(b.depthNear>0&&(fe=b.depthNear),b.depthFar>0&&(ke=b.depthFar)),J.near=q.near=O.near=fe,J.far=q.far=O.far=ke,(H!==J.near||te!==J.far)&&(s.updateRenderState({depthNear:J.near,depthFar:J.far}),H=J.near,te=J.far),J.layers.mask=le.layers.mask|6,O.layers.mask=J.layers.mask&-5,q.layers.mask=J.layers.mask&-3;let st=le.parent,Be=J.cameras;Ye(J,st);for(let ut=0;ut<Be.length;ut++)Ye(Be[ut],st);Be.length===2?ge(J,O,q):J.projectionMatrix.copy(O.projectionMatrix),D===null&&le.isPerspectiveCamera&&(D={camera:le,fov:le.fov,zoom:le.zoom}),$e(le,J,st)};function $e(le,fe,ke){ke===null?le.matrix.copy(fe.matrixWorld):(le.matrix.copy(ke.matrixWorld),le.matrix.invert(),le.matrix.multiply(fe.matrixWorld)),le.matrix.decompose(le.position,le.quaternion,le.scale),le.updateMatrixWorld(!0),le.projectionMatrix.copy(fe.projectionMatrix),le.projectionMatrixInverse.copy(fe.projectionMatrixInverse),le.isPerspectiveCamera&&(le.fov=Lr*2*Math.atan(1/le.projectionMatrix.elements[5]),le.zoom=1)}this.getCamera=function(){return J},this.getFoveation=function(){if(!(m===null&&S===null))return d},this.setFoveation=function(le){d=le,m!==null&&(m.fixedFoveation=le),S!==null&&S.fixedFoveation!==void 0&&(S.fixedFoveation=le)},this.hasDepthSensing=function(){return b.texture!==null},this.getDepthSensingMesh=function(){return b.getMesh(J)},this.getCameraTexture=function(le){return _[le]};let Ut=null;function mt(le,fe){if(g=fe.getViewerPose(f||l),T=fe,g!==null){let ke=g.views;S!==null&&(e.setRenderTargetFramebuffer(R,S.framebuffer),e.setRenderTarget(R));let st=!1;ke.length!==J.cameras.length&&(J.cameras.length=0,st=!0);for(let dt=0;dt<ke.length;dt++){let gt=ke[dt],rt=null;if(S!==null)rt=S.getViewport(gt);else{let St=y.getViewSubImage(m,gt);rt=St.viewport,dt===0&&(e.setRenderTargetTextures(R,St.colorTexture,St.depthStencilTexture),e.setRenderTarget(R))}let tt=Y[dt];tt===void 0&&(tt=new fn,tt.layers.enable(dt),tt.viewport=new Ht,Y[dt]=tt),tt.matrix.fromArray(gt.transform.matrix),tt.matrix.decompose(tt.position,tt.quaternion,tt.scale),tt.projectionMatrix.fromArray(gt.projectionMatrix),tt.projectionMatrixInverse.copy(tt.projectionMatrix).invert(),tt.viewport.set(rt.x,rt.y,rt.width,rt.height),dt===0&&(J.matrix.copy(tt.matrix),J.matrix.decompose(J.position,J.quaternion,J.scale)),st===!0&&J.cameras.push(tt)}let Be=s.enabledFeatures;if(Be&&Be.includes("depth-sensing")&&s.depthUsage=="gpu-optimized"&&P){y=n.getBinding();let dt=y.getDepthInformation(ke[0]);dt&&dt.isValid&&dt.texture&&b.init(dt,s.renderState)}if(Be&&Be.includes("camera-access")&&P){e.state.unbindTexture(),y=n.getBinding();for(let dt=0;dt<ke.length;dt++){let gt=ke[dt].camera;if(gt){let rt=_[gt];rt||(rt=new xs,_[gt]=rt);let tt=y.getCameraImage(gt);rt.sourceTexture=tt}}}}for(let ke=0;ke<I.length;ke++){let st=L[ke],Be=I[ke];st!==null&&Be!==void 0&&Be.update(st,fe,f||l)}Ut&&Ut(le,fe),fe.detectedPlanes&&n.dispatchEvent({type:"planesdetected",data:fe}),T=null}let Ke=new Cd;Ke.setAnimationLoop(mt),this.setAnimationLoop=function(le){Ut=le},this.dispose=function(){}}},Fb=new Ot,Fd=new at;Fd.set(-1,0,0,0,1,0,0,0,1);function Nb(i,e){function t(b,_){b.matrixAutoUpdate===!0&&b.updateMatrix(),_.value.copy(b.matrix)}function n(b,_){_.color.getRGB(b.fogColor.value,Nc(i)),_.isFog?(b.fogNear.value=_.near,b.fogFar.value=_.far):_.isFogExp2&&(b.fogDensity.value=_.density)}function s(b,_,U,z,R){_.isNodeMaterial?_.uniformsNeedUpdate=!1:_.isMeshBasicMaterial?o(b,_):_.isMeshLambertMaterial?(o(b,_),_.envMap&&(b.envMapIntensity.value=_.envMapIntensity)):_.isMeshToonMaterial?(o(b,_),y(b,_)):_.isMeshPhongMaterial?(o(b,_),g(b,_),_.envMap&&(b.envMapIntensity.value=_.envMapIntensity)):_.isMeshStandardMaterial?(o(b,_),m(b,_),_.isMeshPhysicalMaterial&&S(b,_,R)):_.isMeshMatcapMaterial?(o(b,_),T(b,_)):_.isMeshDepthMaterial?o(b,_):_.isMeshDistanceMaterial?(o(b,_),P(b,_)):_.isMeshNormalMaterial?o(b,_):_.isLineBasicMaterial?(l(b,_),_.isLineDashedMaterial&&h(b,_)):_.isPointsMaterial?d(b,_,U,z):_.isSpriteMaterial?f(b,_):_.isShadowMaterial?(b.color.value.copy(_.color),b.opacity.value=_.opacity):_.isShaderMaterial&&(_.uniformsNeedUpdate=!1)}function o(b,_){b.opacity.value=_.opacity,_.color&&b.diffuse.value.copy(_.color),_.emissive&&b.emissive.value.copy(_.emissive).multiplyScalar(_.emissiveIntensity),_.map&&(b.map.value=_.map,t(_.map,b.mapTransform)),_.alphaMap&&(b.alphaMap.value=_.alphaMap,t(_.alphaMap,b.alphaMapTransform)),_.bumpMap&&(b.bumpMap.value=_.bumpMap,t(_.bumpMap,b.bumpMapTransform),b.bumpScale.value=_.bumpScale,_.side===xn&&(b.bumpScale.value*=-1)),_.normalMap&&(b.normalMap.value=_.normalMap,t(_.normalMap,b.normalMapTransform),b.normalScale.value.copy(_.normalScale),_.side===xn&&b.normalScale.value.negate()),_.displacementMap&&(b.displacementMap.value=_.displacementMap,t(_.displacementMap,b.displacementMapTransform),b.displacementScale.value=_.displacementScale,b.displacementBias.value=_.displacementBias),_.emissiveMap&&(b.emissiveMap.value=_.emissiveMap,t(_.emissiveMap,b.emissiveMapTransform)),_.specularMap&&(b.specularMap.value=_.specularMap,t(_.specularMap,b.specularMapTransform)),_.alphaTest>0&&(b.alphaTest.value=_.alphaTest);let U=e.get(_),z=U.envMap,R=U.envMapRotation;z&&(b.envMap.value=z,b.envMapRotation.value.setFromMatrix4(Fb.makeRotationFromEuler(R)).transpose(),z.isCubeTexture&&z.isRenderTargetTexture===!1&&b.envMapRotation.value.premultiply(Fd),b.reflectivity.value=_.reflectivity,b.ior.value=_.ior,b.refractionRatio.value=_.refractionRatio),_.lightMap&&(b.lightMap.value=_.lightMap,b.lightMapIntensity.value=_.lightMapIntensity,t(_.lightMap,b.lightMapTransform)),_.aoMap&&(b.aoMap.value=_.aoMap,b.aoMapIntensity.value=_.aoMapIntensity,t(_.aoMap,b.aoMapTransform))}function l(b,_){b.diffuse.value.copy(_.color),b.opacity.value=_.opacity,_.map&&(b.map.value=_.map,t(_.map,b.mapTransform))}function h(b,_){b.dashSize.value=_.dashSize,b.totalSize.value=_.dashSize+_.gapSize,b.scale.value=_.scale}function d(b,_,U,z){b.diffuse.value.copy(_.color),b.opacity.value=_.opacity,b.size.value=_.size*U,b.scale.value=z*.5,_.map&&(b.map.value=_.map,t(_.map,b.uvTransform)),_.alphaMap&&(b.alphaMap.value=_.alphaMap,t(_.alphaMap,b.alphaMapTransform)),_.alphaTest>0&&(b.alphaTest.value=_.alphaTest)}function f(b,_){b.diffuse.value.copy(_.color),b.opacity.value=_.opacity,b.rotation.value=_.rotation,_.map&&(b.map.value=_.map,t(_.map,b.mapTransform)),_.alphaMap&&(b.alphaMap.value=_.alphaMap,t(_.alphaMap,b.alphaMapTransform)),_.alphaTest>0&&(b.alphaTest.value=_.alphaTest)}function g(b,_){b.specular.value.copy(_.specular),b.shininess.value=Math.max(_.shininess,1e-4)}function y(b,_){_.gradientMap&&(b.gradientMap.value=_.gradientMap)}function m(b,_){b.metalness.value=_.metalness,_.metalnessMap&&(b.metalnessMap.value=_.metalnessMap,t(_.metalnessMap,b.metalnessMapTransform)),b.roughness.value=_.roughness,_.roughnessMap&&(b.roughnessMap.value=_.roughnessMap,t(_.roughnessMap,b.roughnessMapTransform)),_.envMap&&(b.envMapIntensity.value=_.envMapIntensity)}function S(b,_,U){b.ior.value=_.ior,_.sheen>0&&(b.sheenColor.value.copy(_.sheenColor).multiplyScalar(_.sheen),b.sheenRoughness.value=_.sheenRoughness,_.sheenColorMap&&(b.sheenColorMap.value=_.sheenColorMap,t(_.sheenColorMap,b.sheenColorMapTransform)),_.sheenRoughnessMap&&(b.sheenRoughnessMap.value=_.sheenRoughnessMap,t(_.sheenRoughnessMap,b.sheenRoughnessMapTransform))),_.clearcoat>0&&(b.clearcoat.value=_.clearcoat,b.clearcoatRoughness.value=_.clearcoatRoughness,_.clearcoatMap&&(b.clearcoatMap.value=_.clearcoatMap,t(_.clearcoatMap,b.clearcoatMapTransform)),_.clearcoatRoughnessMap&&(b.clearcoatRoughnessMap.value=_.clearcoatRoughnessMap,t(_.clearcoatRoughnessMap,b.clearcoatRoughnessMapTransform)),_.clearcoatNormalMap&&(b.clearcoatNormalMap.value=_.clearcoatNormalMap,t(_.clearcoatNormalMap,b.clearcoatNormalMapTransform),b.clearcoatNormalScale.value.copy(_.clearcoatNormalScale),_.side===xn&&b.clearcoatNormalScale.value.negate())),_.dispersion>0&&(b.dispersion.value=_.dispersion),_.retroreflectivity>0&&(b.retroreflectivity.value=_.retroreflectivity),_.iridescence>0&&(b.iridescence.value=_.iridescence,b.iridescenceIOR.value=_.iridescenceIOR,b.iridescenceThicknessMinimum.value=_.iridescenceThicknessRange[0],b.iridescenceThicknessMaximum.value=_.iridescenceThicknessRange[1],_.iridescenceMap&&(b.iridescenceMap.value=_.iridescenceMap,t(_.iridescenceMap,b.iridescenceMapTransform)),_.iridescenceThicknessMap&&(b.iridescenceThicknessMap.value=_.iridescenceThicknessMap,t(_.iridescenceThicknessMap,b.iridescenceThicknessMapTransform))),_.transmission>0&&(b.transmission.value=_.transmission,b.transmissionSamplerMap.value=U.texture,b.transmissionSamplerSize.value.set(U.width,U.height),_.transmissionMap&&(b.transmissionMap.value=_.transmissionMap,t(_.transmissionMap,b.transmissionMapTransform)),b.thickness.value=_.thickness,_.thicknessMap&&(b.thicknessMap.value=_.thicknessMap,t(_.thicknessMap,b.thicknessMapTransform)),b.attenuationDistance.value=_.attenuationDistance,b.attenuationColor.value.copy(_.attenuationColor)),_.anisotropy>0&&(b.anisotropyVector.value.set(_.anisotropy*Math.cos(_.anisotropyRotation),_.anisotropy*Math.sin(_.anisotropyRotation)),_.anisotropyMap&&(b.anisotropyMap.value=_.anisotropyMap,t(_.anisotropyMap,b.anisotropyMapTransform))),b.specularIntensity.value=_.specularIntensity,b.specularColor.value.copy(_.specularColor),_.specularColorMap&&(b.specularColorMap.value=_.specularColorMap,t(_.specularColorMap,b.specularColorMapTransform)),_.specularIntensityMap&&(b.specularIntensityMap.value=_.specularIntensityMap,t(_.specularIntensityMap,b.specularIntensityMapTransform))}function T(b,_){_.matcap&&(b.matcap.value=_.matcap)}function P(b,_){let U=e.get(_).light;b.referencePosition.value.setFromMatrixPosition(U.matrixWorld),b.nearDistance.value=U.shadow.camera.near,b.farDistance.value=U.shadow.camera.far}return{refreshFogUniforms:n,refreshMaterialUniforms:s}}function Ub(i,e,t,n){let s={},o={},l=[],h=i.getParameter(i.MAX_UNIFORM_BUFFER_BINDINGS);function d(R,I){let L=I.program;n.uniformBlockBinding(R,L)}function f(R,I){let L=s[R.id];L===void 0&&(b(R),L=g(R),s[R.id]=L,R.addEventListener("dispose",U));let B=I.program;n.updateUBOMapping(R,B);let w=e.render.frame;o[R.id]!==w&&(m(R),o[R.id]=w)}function g(R){let I=y();R.__bindingPointIndex=I;let L=i.createBuffer(),B=R.__size,w=R.usage;return i.bindBuffer(i.UNIFORM_BUFFER,L),i.bufferData(i.UNIFORM_BUFFER,B,w),i.bindBuffer(i.UNIFORM_BUFFER,null),i.bindBufferBase(i.UNIFORM_BUFFER,I,L),L}function y(){for(let R=0;R<h;R++)if(l.indexOf(R)===-1)return l.push(R),R;return it("WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function m(R){let I=s[R.id],L=R.uniforms,B=R.__cache;i.bindBuffer(i.UNIFORM_BUFFER,I);for(let w=0,D=L.length;w<D;w++){let O=L[w];if(Array.isArray(O))for(let q=0,Y=O.length;q<Y;q++)S(O[q],w,q,B);else S(O,w,0,B)}i.bindBuffer(i.UNIFORM_BUFFER,null)}function S(R,I,L,B){if(P(R,I,L,B)===!0){let w=R.__offset,D=R.value;if(Array.isArray(D)){let O=0;for(let q=0;q<D.length;q++){let Y=D[q],J=_(Y);T(Y,R.__data,O),typeof Y!="number"&&typeof Y!="boolean"&&!Y.isMatrix3&&!ArrayBuffer.isView(Y)&&(O+=J.storage/Float32Array.BYTES_PER_ELEMENT)}}else T(D,R.__data,0);i.bufferSubData(i.UNIFORM_BUFFER,w,R.__data)}}function T(R,I,L){typeof R=="number"||typeof R=="boolean"?I[0]=R:R.isMatrix3?(I[0]=R.elements[0],I[1]=R.elements[1],I[2]=R.elements[2],I[3]=0,I[4]=R.elements[3],I[5]=R.elements[4],I[6]=R.elements[5],I[7]=0,I[8]=R.elements[6],I[9]=R.elements[7],I[10]=R.elements[8],I[11]=0):ArrayBuffer.isView(R)?I.set(new R.constructor(R.buffer,R.byteOffset,I.length)):R.toArray(I,L)}function P(R,I,L,B){let w=R.value,D=I+"_"+L;if(B[D]===void 0)return typeof w=="number"||typeof w=="boolean"?B[D]=w:ArrayBuffer.isView(w)?B[D]=w.slice():B[D]=w.clone(),!0;{let O=B[D];if(typeof w=="number"||typeof w=="boolean"){if(O!==w)return B[D]=w,!0}else{if(ArrayBuffer.isView(w))return!0;if(O.equals(w)===!1)return O.copy(w),!0}}return!1}function b(R){let I=R.uniforms,L=0,B=16;for(let D=0,O=I.length;D<O;D++){let q=Array.isArray(I[D])?I[D]:[I[D]];for(let Y=0,J=q.length;Y<J;Y++){let H=q[Y],te=Array.isArray(H.value)?H.value:[H.value];for(let k=0,se=te.length;k<se;k++){let _e=te[k],ae=_(_e),V=L%B,ge=V%ae.boundary,Ye=V+ge;L+=ge,Ye!==0&&B-Ye<ae.storage&&(L+=B-Ye),H.__data=new Float32Array(ae.storage/Float32Array.BYTES_PER_ELEMENT),H.__offset=L,L+=ae.storage}}}let w=L%B;return w>0&&(L+=B-w),R.__size=L,R.__cache={},this}function _(R){let I={boundary:0,storage:0};return typeof R=="number"||typeof R=="boolean"?(I.boundary=4,I.storage=4):R.isVector2?(I.boundary=8,I.storage=8):R.isVector3||R.isColor?(I.boundary=16,I.storage=12):R.isVector4?(I.boundary=16,I.storage=16):R.isMatrix3?(I.boundary=48,I.storage=48):R.isMatrix4?(I.boundary=64,I.storage=64):R.isTexture?et("WebGLRenderer: Texture samplers can not be part of an uniforms group."):ArrayBuffer.isView(R)?(I.boundary=16,I.storage=R.byteLength):et("WebGLRenderer: Unsupported uniform value type.",R),I}function U(R){let I=R.target;I.removeEventListener("dispose",U);let L=l.indexOf(I.__bindingPointIndex);l.splice(L,1),i.deleteBuffer(s[I.id]),delete s[I.id],delete o[I.id]}function z(){for(let R in s)i.deleteBuffer(s[R]);l=[],s={},o={}}return{bind:d,update:f,dispose:z}}var Ob=new Uint16Array([12469,15057,12620,14925,13266,14620,13807,14376,14323,13990,14545,13625,14713,13328,14840,12882,14931,12528,14996,12233,15039,11829,15066,11525,15080,11295,15085,10976,15082,10705,15073,10495,13880,14564,13898,14542,13977,14430,14158,14124,14393,13732,14556,13410,14702,12996,14814,12596,14891,12291,14937,11834,14957,11489,14958,11194,14943,10803,14921,10506,14893,10278,14858,9960,14484,14039,14487,14025,14499,13941,14524,13740,14574,13468,14654,13106,14743,12678,14818,12344,14867,11893,14889,11509,14893,11180,14881,10751,14852,10428,14812,10128,14765,9754,14712,9466,14764,13480,14764,13475,14766,13440,14766,13347,14769,13070,14786,12713,14816,12387,14844,11957,14860,11549,14868,11215,14855,10751,14825,10403,14782,10044,14729,9651,14666,9352,14599,9029,14967,12835,14966,12831,14963,12804,14954,12723,14936,12564,14917,12347,14900,11958,14886,11569,14878,11247,14859,10765,14828,10401,14784,10011,14727,9600,14660,9289,14586,8893,14508,8533,15111,12234,15110,12234,15104,12216,15092,12156,15067,12010,15028,11776,14981,11500,14942,11205,14902,10752,14861,10393,14812,9991,14752,9570,14682,9252,14603,8808,14519,8445,14431,8145,15209,11449,15208,11451,15202,11451,15190,11438,15163,11384,15117,11274,15055,10979,14994,10648,14932,10343,14871,9936,14803,9532,14729,9218,14645,8742,14556,8381,14461,8020,14365,7603,15273,10603,15272,10607,15267,10619,15256,10631,15231,10614,15182,10535,15118,10389,15042,10167,14963,9787,14883,9447,14800,9115,14710,8665,14615,8318,14514,7911,14411,7507,14279,7198,15314,9675,15313,9683,15309,9712,15298,9759,15277,9797,15229,9773,15166,9668,15084,9487,14995,9274,14898,8910,14800,8539,14697,8234,14590,7790,14479,7409,14367,7067,14178,6621,15337,8619,15337,8631,15333,8677,15325,8769,15305,8871,15264,8940,15202,8909,15119,8775,15022,8565,14916,8328,14804,8009,14688,7614,14569,7287,14448,6888,14321,6483,14088,6171,15350,7402,15350,7419,15347,7480,15340,7613,15322,7804,15287,7973,15229,8057,15148,8012,15046,7846,14933,7611,14810,7357,14682,7069,14552,6656,14421,6316,14251,5948,14007,5528,15356,5942,15356,5977,15353,6119,15348,6294,15332,6551,15302,6824,15249,7044,15171,7122,15070,7050,14949,6861,14818,6611,14679,6349,14538,6067,14398,5651,14189,5311,13935,4958,15359,4123,15359,4153,15356,4296,15353,4646,15338,5160,15311,5508,15263,5829,15188,6042,15088,6094,14966,6001,14826,5796,14678,5543,14527,5287,14377,4985,14133,4586,13869,4257,15360,1563,15360,1642,15358,2076,15354,2636,15341,3350,15317,4019,15273,4429,15203,4732,15105,4911,14981,4932,14836,4818,14679,4621,14517,4386,14359,4156,14083,3795,13808,3437,15360,122,15360,137,15358,285,15355,636,15344,1274,15322,2177,15281,2765,15215,3223,15120,3451,14995,3569,14846,3567,14681,3466,14511,3305,14344,3121,14037,2800,13753,2467,15360,0,15360,1,15359,21,15355,89,15346,253,15325,479,15287,796,15225,1148,15133,1492,15008,1749,14856,1882,14685,1886,14506,1783,14324,1608,13996,1398,13702,1183]),ui=null;function Bb(){return ui===null&&(ui=new Ya(Ob,16,16,Hi,ei),ui.name="DFG_LUT",ui.minFilter=ln,ui.magFilter=ln,ui.wrapS=si,ui.wrapT=si,ui.generateMipmaps=!1,ui.needsUpdate=!0),ui}var ul=class{constructor(e={}){let{canvas:t=Qu(),context:n=null,depth:s=!0,stencil:o=!1,alpha:l=!1,antialias:h=!1,premultipliedAlpha:d=!0,preserveDrawingBuffer:f=!1,powerPreference:g="default",failIfMajorPerformanceCaveat:y=!1,reversedDepthBuffer:m=!1,outputBufferType:S=En}=e;this.isWebGLRenderer=!0;let T;if(n!==null){if(typeof WebGLRenderingContext<"u"&&n instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");T=n.getContextAttributes().alpha}else T=l;let P=S,b=new Set([Ao,To,wo]),_=new Set([En,Kn,Xr,$r,Mo,Eo]),U=new Uint32Array(4),z=new Int32Array(4),R=new j,I=null,L=null,B=[],w=[],D=null;this.domElement=t,this.debug={checkShaderErrors:!0,diagnostics:{keywords:!1},onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=Jn,this.toneMappingExposure=1,this.transmissionResolutionScale=1;let O=this,q=!1,Y=null,J=null,H=null,te=null;this._outputColorSpace=dn;let k=0,se=0,_e=null,ae=-1,V=null,ge=new Ht,Ye=new Ht,$e=null,Ut=new ht(0),mt=0,Ke=t.width,le=t.height,fe=1,ke=null,st=null,Be=new Ht(0,0,Ke,le),ut=new Ht(0,0,Ke,le),$t=!1,dt=new Br,gt=!1,rt=!1,tt=new Ot,St=new j,Bt=new Ht,Ie={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0},Ue=!1;function Vt(){return _e===null?fe:1}let W=n;function Dt(A,G){return t.getContext(A,G)}let Ct,F,x,Z,ne,oe,Ee,Ae,re,he,Ce,Xe,xe,Te,He,Je,ot,X,Re,de,Pe,Ne,me;try{let A={alpha:!0,depth:s,stencil:o,antialias:h,premultipliedAlpha:d,preserveDrawingBuffer:f,powerPreference:g,failIfMajorPerformanceCaveat:y};if("setAttribute"in t&&t.setAttribute("data-engine",`three.js r${"186"}`),t.addEventListener("webglcontextlost",Ft,!1),t.addEventListener("webglcontextrestored",wt,!1),t.addEventListener("webglcontextcreationerror",Tn,!1),W===null){let G="webgl2";if(W=Dt(G,A),W===null)throw Dt(G)?new Error("THREE.WebGLRenderer: Error creating WebGL context with your selected attributes."):new Error("THREE.WebGLRenderer: Error creating WebGL context.")}je()}catch(A){throw t.removeEventListener("webglcontextlost",Ft,!1),t.removeEventListener("webglcontextrestored",wt,!1),t.removeEventListener("webglcontextcreationerror",Tn,!1),it("WebGLRenderer: "+A.message),A}function je(){Ct=new Xx(W),Ct.init(),Pe=new Ib(W,Ct),F=new Nx(W,Ct,e,Pe),x=new Rb(W,Ct),F.reversedDepthBuffer&&m&&x.buffers.depth.setReversed(!0),J=W.createFramebuffer(),H=W.createFramebuffer(),te=W.createFramebuffer(),Z=new qx(W),ne=new mb,oe=new Pb(W,Ct,x,ne,F,Pe,Z),Ee=new Wx(O),Ae=new Z0(W),Ne=new Lx(W,Ae),re=new $x(W,Ae,Z,Ne),he=new Zx(W,re,Ae,Ne,Z),X=new Yx(W,F,oe),He=new Ux(ne),Ce=new pb(O,Ee,Ct,F,Ne,He),Xe=new Nb(O,ne),xe=new _b,Te=new Mb(Ct),ot=new Dx(O,Ee,x,he,T,d),Je=new Cb(O,he,F),me=new Ub(W,Z,F,x),Re=new Fx(W,Ct,Z),de=new jx(W,Ct,Z),Z.programs=Ce.programs,O.capabilities=F,O.extensions=Ct,O.properties=ne,O.renderLists=xe,O.shadowMap=Je,O.state=x,O.info=Z}P!==En&&(D=new Kx(P,t.width,t.height,h,s,o));let We=new Qc(O,W);this.xr=We,this.getContext=function(){return W},this.getContextAttributes=function(){return W.getContextAttributes()},this.forceContextLoss=function(){let A=Ct.get("WEBGL_lose_context");A&&A.loseContext()},this.forceContextRestore=function(){let A=Ct.get("WEBGL_lose_context");A&&A.restoreContext()},this.getPixelRatio=function(){return fe},this.setPixelRatio=function(A){A!==void 0&&(fe=A,this.setSize(Ke,le,!1))},this.getSize=function(A){return A.set(Ke,le)},this.setSize=function(A,G,ie=!0){if(We.isPresenting){et("WebGLRenderer: Can't change size while VR device is presenting.");return}Ke=A,le=G,t.width=Math.floor(A*fe),t.height=Math.floor(G*fe),ie===!0&&(t.style.width=A+"px",t.style.height=G+"px"),D!==null&&D.setSize(t.width,t.height),this.setViewport(0,0,A,G)},this.getDrawingBufferSize=function(A){return A.set(Ke*fe,le*fe).floor()},this.setDrawingBufferSize=function(A,G,ie){Ke=A,le=G,fe=ie,t.width=Math.floor(A*ie),t.height=Math.floor(G*ie),this.setViewport(0,0,A,G)},this.setEffects=function(A){if(P===En){it("WebGLRenderer: setEffects() requires outputBufferType set to HalfFloatType or FloatType.");return}if(A){for(let G=0;G<A.length;G++)if(A[G].isOutputPass===!0){et("WebGLRenderer: OutputPass is not needed in setEffects(). Tone mapping and color space conversion are applied automatically.");break}}D.setEffects(A||[])},this.getCurrentViewport=function(A){return A.copy(ge)},this.getViewport=function(A){return A.copy(Be)},this.setViewport=function(A,G,ie,K){A.isVector4?Be.set(A.x,A.y,A.z,A.w):Be.set(A,G,ie,K),x.viewport(ge.copy(Be).multiplyScalar(fe).round())},this.getScissor=function(A){return A.copy(ut)},this.setScissor=function(A,G,ie,K){A.isVector4?ut.set(A.x,A.y,A.z,A.w):ut.set(A,G,ie,K),x.scissor(Ye.copy(ut).multiplyScalar(fe).round())},this.getScissorTest=function(){return $t},this.setScissorTest=function(A){x.setScissorTest($t=A)},this.setOpaqueSort=function(A){ke=A},this.setTransparentSort=function(A){st=A},this.getClearColor=function(A){return A.copy(ot.getClearColor())},this.setClearColor=function(){ot.setClearColor(...arguments)},this.getClearAlpha=function(){return ot.getClearAlpha()},this.setClearAlpha=function(){ot.setClearAlpha(...arguments)},this.clear=function(A=!0,G=!0,ie=!0){let K=0;if(A){let Q=!1;if(_e!==null){let Le=_e.texture.format;Q=b.has(Le)}if(Q){let Le=_e.texture.type,be=_.has(Le),De=ot.getClearColor(),Ve=ot.getClearAlpha(),ze=De.r,lt=De.g,ct=De.b;be?(U[0]=ze,U[1]=lt,U[2]=ct,U[3]=Ve,W.clearBufferuiv(W.COLOR,0,U)):(z[0]=ze,z[1]=lt,z[2]=ct,z[3]=Ve,W.clearBufferiv(W.COLOR,0,z))}else K|=W.COLOR_BUFFER_BIT}G&&(K|=W.DEPTH_BUFFER_BIT,this.state.buffers.depth.setMask(!0)),ie&&(K|=W.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),K!==0&&W.clear(K)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.setNodesHandler=function(A){A.setRenderer(this),Y=A},this.dispose=function(){t.removeEventListener("webglcontextlost",Ft,!1),t.removeEventListener("webglcontextrestored",wt,!1),t.removeEventListener("webglcontextcreationerror",Tn,!1),ot.dispose(),xe.dispose(),Te.dispose(),ne.dispose(),Ee.dispose(),he.dispose(),Ne.dispose(),me.dispose(),Ce.dispose(),We.dispose(),We.removeEventListener("sessionstart",Vn),We.removeEventListener("sessionend",Kr),Sn.stop()};function Ft(A){A.preventDefault(),Dc("WebGLRenderer: Context Lost."),q=!0}function wt(){Dc("WebGLRenderer: Context Restored."),q=!1;let A=Z.autoReset,G=Je.enabled,ie=Je.autoUpdate,K=Je.needsUpdate,Q=Je.type;je(),Z.autoReset=A,Je.enabled=G,Je.autoUpdate=ie,Je.needsUpdate=K,Je.type=Q}function Tn(A){it("WebGLRenderer: A WebGL context could not be created. Reason: ",A.statusMessage)}function zn(A){let G=A.target;G.removeEventListener("dispose",zn),Ws(G)}function Ws(A){Mi(A),ne.remove(A)}function Mi(A){let G=ne.get(A).programs;G!==void 0&&(G.forEach(function(ie){Ce.releaseProgram(ie)}),A.isShaderMaterial&&Ce.releaseShaderCache(A))}this.renderBufferDirect=function(A,G,ie,K,Q,Le){G===null&&(G=Ie);let be=Q.isMesh&&Q.matrixWorld.determinantAffine()<0,De=dr(A,G,ie,K,Q);x.setMaterial(K,be);let Ve=ie.index,ze=1;if(K.wireframe===!0){if(Ve=re.getWireframeAttribute(ie),Ve===void 0)return;ze=2}let lt=ie.drawRange,ct=ie.attributes.position,Ge=lt.start*ze,Et=(lt.start+lt.count)*ze;Le!==null&&(Ge=Math.max(Ge,Le.start*ze),Et=Math.min(Et,(Le.start+Le.count)*ze)),Ve!==null?(Ge=Math.max(Ge,0),Et=Math.min(Et,Ve.count)):ct!=null&&(Ge=Math.max(Ge,0),Et=Math.min(Et,ct.count));let jt=Et-Ge;if(jt<0||jt===1/0)return;Ne.setup(Q,K,De,ie,Ve);let bt,Pt=Re;if(Ve!==null&&(bt=Ae.get(Ve),Pt=de,Pt.setIndex(bt)),Q.isMesh)K.wireframe===!0?(x.setLineWidth(K.wireframeLinewidth*Vt()),Pt.setMode(W.LINES)):Pt.setMode(W.TRIANGLES);else if(Q.isLine){let qe=K.linewidth;qe===void 0&&(qe=1),x.setLineWidth(qe*Vt()),Q.isLineSegments?Pt.setMode(W.LINES):Q.isLineLoop?Pt.setMode(W.LINE_LOOP):Pt.setMode(W.LINE_STRIP)}else Q.isPoints?Pt.setMode(W.POINTS):Q.isSprite&&Pt.setMode(W.TRIANGLES);if(Q.isBatchedMesh)if(Ct.get("WEBGL_multi_draw"))Pt.renderMultiDraw(Q._multiDrawStarts,Q._multiDrawCounts,Q._multiDrawCount);else{let qe=Q._multiDrawStarts,Oe=Q._multiDrawCounts,rn=Q._multiDrawCount,Mt=Ve?Ae.get(Ve).bytesPerElement:1,mn=ne.get(K).currentProgram.getUniforms();for(let Un=0;Un<rn;Un++)mn.setValue(W,"_gl_DrawID",Un),Pt.render(qe[Un]/Mt,Oe[Un])}else if(Q.isInstancedMesh)Pt.renderInstances(Ge,jt,Q.count);else if(ie.isInstancedBufferGeometry){let qe=ie._maxInstanceCount!==void 0?ie._maxInstanceCount:1/0,Oe=Math.min(ie.instanceCount,qe);Pt.renderInstances(Ge,jt,Oe)}else Pt.render(Ge,jt)};function gl(A,G,ie,K){Y!==null&&A.isNodeMaterial&&Y.setObject(K,A),gt===!0&&He.setState(A,ie,!1),A.transparent===!0&&A.side===ci&&A.forceSinglePass===!1?(A.side=xn,A.needsUpdate=!0,hr(A,G,K),A.side=li,A.needsUpdate=!0,hr(A,G,K),A.side=ci):hr(A,G,K)}this.compile=function(A,G,ie=null){ie===null&&(ie=A),Y!==null&&Y.renderStart(A,G,ie),L=Te.get(ie),L.init(G),w.push(L),ie.traverseVisible(function(Q){Q.isLight&&Q.layers.test(G.layers)&&(L.pushLight(Q),Q.castShadow&&L.pushShadow(Q))}),A!==ie&&A.traverseVisible(function(Q){Q.isLight&&Q.layers.test(G.layers)&&(L.pushLight(Q),Q.castShadow&&L.pushShadow(Q))}),L.setupLights(),Y!==null&&Y.updateLights(L.state.lightsArray),rt=this.localClippingEnabled,gt=He.init(this.clippingPlanes,rt),gt===!0&&He.setGlobalState(this.clippingPlanes,G),Y!==null&&Je.render(L.state.shadowsArray,ie,G);let K=new Set;return A.traverse(function(Q){if(!(Q.isMesh||Q.isPoints||Q.isLine||Q.isSprite))return;let Le=Q.material;if(Le)if(Array.isArray(Le))for(let be=0;be<Le.length;be++){let De=Le[be];gl(De,ie,G,Q),K.add(De)}else gl(Le,ie,G,Q),K.add(Le)}),L=w.pop(),Y!==null&&Y.renderEnd(),K},this.compileAsync=function(A,G,ie=null){let K=this.compile(A,G,ie);return new Promise(Q=>{function Le(){if(K.forEach(function(be){let Ve=ne.get(be).currentProgram;(Ve===void 0||Ve.isReady())&&K.delete(be)}),K.size===0){Q(A);return}setTimeout(Le,10)}Ct.get("KHR_parallel_shader_compile")!==null?Le():setTimeout(Le,10)})};let ye=null;function Se(A){ye&&ye(A)}function Vn(){Sn.stop()}function Kr(){Sn.start()}let Sn=new Cd;Sn.setAnimationLoop(Se),typeof self<"u"&&Sn.setContext(self),this.setAnimationLoop=function(A){ye=A,We.setAnimationLoop(A),A===null?Sn.stop():Sn.start()},We.addEventListener("sessionstart",Vn),We.addEventListener("sessionend",Kr),this.render=function(A,G){if(G!==void 0&&G.isCamera!==!0){it("WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(q===!0)return;Y!==null&&Y.renderStart(A,G);let ie=We.enabled===!0&&We.isPresenting===!0,K=D!==null&&(_e===null||ie)&&D.begin(O,_e);if(A.matrixWorldAutoUpdate===!0&&A.updateMatrixWorld(),G.parent===null&&G.matrixWorldAutoUpdate===!0&&G.updateMatrixWorld(),We.enabled===!0&&We.isPresenting===!0&&(D===null||D.isCompositing()===!1)&&(We.cameraAutoUpdate===!0&&We.updateCamera(G),G=We.getCamera()),A.isScene===!0&&A.onBeforeRender(O,A,G,_e),L=Te.get(A,w.length),L.init(G),L.state.textureUnits=oe.getTextureUnits(),w.push(L),tt.multiplyMatrices(G.projectionMatrix,G.matrixWorldInverse),dt.setFromProjectionMatrix(tt,Yn,G.reversedDepth),rt=this.localClippingEnabled,gt=He.init(this.clippingPlanes,rt),I=xe.get(A,B.length),I.init(),B.push(I),We.enabled===!0&&We.isPresenting===!0){let be=O.xr.getDepthSensingMesh();be!==null&&An(be,G,-1/0,O.sortObjects)}An(A,G,0,O.sortObjects),I.finish(),Y!==null&&Y.updateLights(L.state.lightsArray),O.sortObjects===!0&&I.sort(ke,st),Ue=We.enabled===!1||We.isPresenting===!1||We.hasDepthSensing()===!1,Ue&&ot.addToRenderList(I,A),this.info.render.frame++,this.info.autoReset===!0&&this.info.reset(),gt===!0&&He.beginShadows();let Q=L.state.shadowsArray;if(Je.render(Q,A,G),gt===!0&&He.endShadows(),(K&&D.hasRenderPass())===!1){let be=I.opaque,De=I.transmissive;if(L.setupLights(),G.isArrayCamera){let Ve=G.cameras;if(De.length>0)for(let ze=0,lt=Ve.length;ze<lt;ze++){let ct=Ve[ze];Fn(be,De,A,ct)}Ue&&ot.render(A);for(let ze=0,lt=Ve.length;ze<lt;ze++){let ct=Ve[ze];Xs(I,A,ct,ct.viewport)}}else De.length>0&&Fn(be,De,A,G),Ue&&ot.render(A),Xs(I,A,G)}_e!==null&&se===0&&(oe.updateMultisampleRenderTarget(_e),oe.updateRenderTargetMipmap(_e)),K&&D.end(O),A.isScene===!0&&A.onAfterRender(O,A,G),Ne.resetDefaultState(),ae=-1,V=null,w.pop(),w.length>0?(L=w[w.length-1],oe.setTextureUnits(L.state.textureUnits),gt===!0&&He.setGlobalState(O.clippingPlanes,L.state.camera)):L=null,B.pop(),B.length>0?I=B[B.length-1]:I=null,Y!==null&&Y.renderEnd()};function An(A,G,ie,K){if(A.visible===!1)return;if(A.layers.test(G.layers)){if(A.isGroup)ie=A.renderOrder;else if(A.isLOD)A.autoUpdate===!0&&A.update(G);else if(A.isLightProbeGrid)L.pushLightProbeGrid(A);else if(A.isLight)L.pushLight(A),A.castShadow&&L.pushShadow(A);else if(A.isSprite){if(!A.frustumCulled||A.intersectsFrustum(dt)){K&&Bt.setFromMatrixPosition(A.matrixWorld).applyMatrix4(tt);let be=he.update(A),De=A.material;De.visible&&I.push(A,be,De,ie,Bt.z,null,G)}}else if((A.isMesh||A.isLine||A.isPoints)&&(!A.frustumCulled||A.intersectsFrustum(dt))){let be=he.update(A),De=A.material;if(K&&(A.boundingSphere!==void 0?(A.boundingSphere===null&&A.computeBoundingSphere(),Bt.copy(A.boundingSphere.center)):(be.boundingSphere===null&&be.computeBoundingSphere(),Bt.copy(be.boundingSphere.center)),Bt.applyMatrix4(A.matrixWorld).applyMatrix4(tt)),Array.isArray(De)){let Ve=be.groups;for(let ze=0,lt=Ve.length;ze<lt;ze++){let ct=Ve[ze],Ge=De[ct.materialIndex];Ge&&Ge.visible&&I.push(A,be,Ge,ie,Bt.z,ct,G)}}else De.visible&&I.push(A,be,De,ie,Bt.z,null,G)}}let Le=A.children;for(let be=0,De=Le.length;be<De;be++)An(Le[be],G,ie,K)}function Xs(A,G,ie,K){let{opaque:Q,transmissive:Le,transparent:be}=A;L.setupLightsView(ie),gt===!0&&He.setGlobalState(O.clippingPlanes,ie),K&&x.viewport(ge.copy(K)),Q.length>0&&fi(Q,G,ie),Le.length>0&&fi(Le,G,ie),be.length>0&&fi(be,G,ie),x.buffers.depth.setTest(!0),x.buffers.depth.setMask(!0),x.buffers.color.setMask(!0),x.setPolygonOffset(!1)}function Fn(A,G,ie,K){if((ie.isScene===!0?ie.overrideMaterial:null)!==null)return;if(L.state.transmissionRenderTarget[K.id]===void 0){let Ge=Ct.has("EXT_color_buffer_half_float")||Ct.has("EXT_color_buffer_float");L.state.transmissionRenderTarget[K.id]=new Mn(1,1,{generateMipmaps:!0,type:Ge?ei:En,minFilter:Vi,samples:Math.max(4,F.samples),stencilBuffer:o,resolveDepthBuffer:!1,resolveStencilBuffer:!1,storeMultisampledDepthBuffer:!1,storeMultisampledStencilBuffer:!1,colorSpace:xt.workingColorSpace})}let Le=L.state.transmissionRenderTarget[K.id],be=K.viewport||ge;Le.setSize(be.z*O.transmissionResolutionScale,be.w*O.transmissionResolutionScale);let De=O.getRenderTarget(),Ve=O.getActiveCubeFace(),ze=O.getActiveMipmapLevel();O.setRenderTarget(Le),O.getClearColor(Ut),mt=O.getClearAlpha(),mt<1&&O.setClearColor(16777215,.5),O.clear(),Ue&&ot.render(ie);let lt=O.toneMapping;O.toneMapping=Jn;let ct=K.viewport;if(K.viewport!==void 0&&(K.viewport=void 0),L.setupLightsView(K),gt===!0&&He.setGlobalState(O.clippingPlanes,K),fi(A,ie,K),oe.updateMultisampleRenderTarget(Le),oe.updateRenderTargetMipmap(Le),Ct.has("WEBGL_multisampled_render_to_texture")===!1){let Ge=!1;for(let Et=0,jt=G.length;Et<jt;Et++){let bt=G[Et],{object:Pt,geometry:qe,material:Oe,group:rn}=bt;if(Oe.side===ci&&Pt.layers.test(K.layers)){let Mt=Oe.side;Oe.side=xn,Oe.needsUpdate=!0,$s(Pt,ie,K,qe,Oe,rn),Oe.side=Mt,Oe.needsUpdate=!0,Ge=!0}}Ge===!0&&(oe.updateMultisampleRenderTarget(Le),oe.updateRenderTargetMipmap(Le))}O.setRenderTarget(De,Ve,ze),O.setClearColor(Ut,mt),ct!==void 0&&(K.viewport=ct),O.toneMapping=lt}function fi(A,G,ie){let K=G.isScene===!0?G.overrideMaterial:null;for(let Q=0,Le=A.length;Q<Le;Q++){let be=A[Q],{object:De,geometry:Ve,group:ze}=be,lt=be.material;lt.allowOverride===!0&&K!==null&&(lt=K),De.layers.test(ie.layers)&&$s(De,G,ie,Ve,lt,ze)}}function $s(A,G,ie,K,Q,Le){Y!==null&&Q.isNodeMaterial&&Y.setObject(A,Q),A.onBeforeRender(O,G,ie,K,Q,Le),A.modelViewMatrix.multiplyMatrices(ie.matrixWorldInverse,A.matrixWorld),A.normalMatrix.getNormalMatrix(A.modelViewMatrix),Q.onBeforeRender(O,G,ie,K,A,Le),Q.transparent===!0&&Q.side===ci&&Q.forceSinglePass===!1?(Q.side=xn,Q.needsUpdate=!0,O.renderBufferDirect(ie,G,K,Q,A,Le),Q.side=li,Q.needsUpdate=!0,O.renderBufferDirect(ie,G,K,Q,A,Le),Q.side=ci):O.renderBufferDirect(ie,G,K,Q,A,Le),A.onAfterRender(O,G,ie,K,Q,Le)}function hr(A,G,ie){G.isScene!==!0&&(G=Ie);let K=ne.get(A),Q=L.state.lights,Le=L.state.shadowsArray,be=Q.state.version,De=Ce.getParameters(A,Q.state,Le,G,ie,L.state.lightProbeGridArray),Ve=Ce.getProgramCacheKey(De),ze=K.programs;K.environment=A.isMeshStandardMaterial||A.isMeshLambertMaterial||A.isMeshPhongMaterial?G.environment:null,K.fog=G.fog;let lt=A.isMeshStandardMaterial||A.isMeshLambertMaterial&&!A.envMap||A.isMeshPhongMaterial&&!A.envMap;K.envMap=Ee.get(A.envMap||K.environment,lt),K.envMapRotation=K.environment!==null&&A.envMap===null?G.environmentRotation:A.envMapRotation,ze===void 0&&(A.addEventListener("dispose",zn),ze=new Map,K.programs=ze);let ct=ze.get(Ve);if(ct!==void 0){if(K.currentProgram===ct&&K.lightsStateVersion===be)return js(A,De),ct}else De.uniforms=Ce.getUniforms(A),Y!==null&&A.isNodeMaterial&&Y.build(A,ie,De),A.onBeforeCompile(De,O),ct=Ce.acquireProgram(De,Ve),ze.set(Ve,ct),K.uniforms=De.uniforms;let Ge=K.uniforms;return(!A.isShaderMaterial&&!A.isRawShaderMaterial||A.clipping===!0)&&(Ge.clippingPlanes=He.uniform),js(A,De),K.needsLights=_l(A),K.lightsStateVersion=be,K.needsLights&&(Ge.ambientLightColor.value=Q.state.ambient,Ge.lightProbe.value=Q.state.probe,Ge.sunLights.value=Q.state.sun,Ge.sunLightShadows.value=Q.state.sunShadow,Ge.directionalLights.value=Q.state.directional,Ge.directionalLightShadows.value=Q.state.directionalShadow,Ge.spotLights.value=Q.state.spot,Ge.spotLightShadows.value=Q.state.spotShadow,Ge.rectAreaLights.value=Q.state.rectArea,Ge.ltc_1.value=Q.state.rectAreaLTC1,Ge.ltc_2.value=Q.state.rectAreaLTC2,Ge.pointLights.value=Q.state.point,Ge.pointLightShadows.value=Q.state.pointShadow,Ge.hemisphereLights.value=Q.state.hemi,Ge.sunShadowMatrix.value=Q.state.sunShadowMatrix,Ge.sunShadowCascade.value=Q.state.sunShadowCascade,Ge.directionalShadowMatrix.value=Q.state.directionalShadowMatrix,Ge.spotLightMatrix.value=Q.state.spotLightMatrix,Ge.spotLightMap.value=Q.state.spotLightMap,Ge.pointShadowMatrix.value=Q.state.pointShadowMatrix),K.lightProbeGrid=L.state.lightProbeGridArray.length>0,K.currentProgram=ct,K.uniformsList=null,ct}function Nn(A){if(A.uniformsList===null){let G=A.currentProgram.getUniforms();A.uniformsList=Zr.seqWithValue(G.seq,A.uniforms)}return A.uniformsList}function js(A,G){let ie=ne.get(A);ie.outputColorSpace=G.outputColorSpace,ie.batching=G.batching,ie.batchingColor=G.batchingColor,ie.instancing=G.instancing,ie.instancingColor=G.instancingColor,ie.instancingMorph=G.instancingMorph,ie.skinning=G.skinning,ie.morphTargets=G.morphTargets,ie.morphNormals=G.morphNormals,ie.morphColors=G.morphColors,ie.morphTargetsCount=G.morphTargetsCount,ie.numClippingPlanes=G.numClippingPlanes,ie.numIntersection=G.numClipIntersection,ie.vertexAlphas=G.vertexAlphas,ie.vertexTangents=G.vertexTangents,ie.toneMapping=G.toneMapping}function ur(A,G){if(A.length===0)return null;if(A.length===1)return A[0].texture!==null?A[0]:null;R.setFromMatrixPosition(G.matrixWorld);for(let ie=0,K=A.length;ie<K;ie++){let Q=A[ie];if(Q.texture!==null&&Q.boundingBox.containsPoint(R))return Q}return null}function dr(A,G,ie,K,Q){G.isScene!==!0&&(G=Ie),oe.resetTextureUnits();let Le=G.fog,be=K.isMeshStandardMaterial||K.isMeshLambertMaterial||K.isMeshPhongMaterial?G.environment:null,De=_e===null?O.outputColorSpace:_e.isXRRenderTarget===!0?_e.texture.colorSpace:xt.workingColorSpace,Ve=K.isMeshStandardMaterial||K.isMeshLambertMaterial&&!K.envMap||K.isMeshPhongMaterial&&!K.envMap,ze=Ee.get(K.envMap||be,Ve),lt=K.vertexColors===!0&&!!ie.attributes.color&&ie.attributes.color.itemSize===4,ct=!!ie.attributes.tangent&&(!!K.normalMap||K.anisotropy>0),Ge=!!ie.morphAttributes.position,Et=!!ie.morphAttributes.normal,jt=!!ie.morphAttributes.color,bt=Jn;K.toneMapped&&(_e===null||_e.isXRRenderTarget===!0)&&(bt=O.toneMapping);let Pt=ie.morphAttributes.position||ie.morphAttributes.normal||ie.morphAttributes.color,qe=Pt!==void 0?Pt.length:0,Oe=ne.get(K),rn=L.state.lights;if(gt===!0&&(rt===!0||A!==V)){let M=A===V&&K.id===ae;He.setState(K,A,M)}let Mt=!1;K.version===Oe.__version?(Oe.needsLights&&Oe.lightsStateVersion!==rn.state.version||Oe.outputColorSpace!==De||Q.isBatchedMesh&&Oe.batching===!1||!Q.isBatchedMesh&&Oe.batching===!0||Q.isBatchedMesh&&Oe.batchingColor===!0&&Q._colorsTexture===null||Q.isBatchedMesh&&Oe.batchingColor===!1&&Q._colorsTexture!==null||Q.isInstancedMesh&&Oe.instancing===!1||!Q.isInstancedMesh&&Oe.instancing===!0||Q.isSkinnedMesh&&Oe.skinning===!1||!Q.isSkinnedMesh&&Oe.skinning===!0||Q.isInstancedMesh&&Oe.instancingColor===!0&&Q.instanceColor===null||Q.isInstancedMesh&&Oe.instancingColor===!1&&Q.instanceColor!==null||Q.isInstancedMesh&&Oe.instancingMorph===!0&&Q.morphTexture===null||Q.isInstancedMesh&&Oe.instancingMorph===!1&&Q.morphTexture!==null||Oe.envMap!==ze||K.fog===!0&&Oe.fog!==Le||Oe.numClippingPlanes!==void 0&&(Oe.numClippingPlanes!==He.numPlanes||Oe.numIntersection!==He.numIntersection)||Oe.vertexAlphas!==lt||Oe.vertexTangents!==ct||Oe.morphTargets!==Ge||Oe.morphNormals!==Et||Oe.morphColors!==jt||Oe.toneMapping!==bt||Oe.morphTargetsCount!==qe||!!Oe.lightProbeGrid!=L.state.lightProbeGridArray.length>0)&&(Mt=!0):(Mt=!0,Oe.__version=K.version);let mn=Oe.currentProgram;Mt===!0&&(mn=hr(K,G,Q),Y&&K.isNodeMaterial&&Y.onUpdateProgram(K,mn,Oe));let Un=!1,Gn=!1,Ei=!1,Rt=mn.getUniforms(),Wt=Oe.uniforms;if(x.useProgram(mn.program)&&(Un=!0,Gn=!0,Ei=!0),K.id!==ae&&(ae=K.id,Gn=!0),Oe.needsLights){let M=ur(L.state.lightProbeGridArray,Q);Oe.lightProbeGrid!==M&&(Oe.lightProbeGrid=M,Gn=!0)}if(Un||V!==A){x.buffers.depth.getReversed()&&A.reversedDepth!==!0&&(A._reversedDepth=!0,A.updateProjectionMatrix()),Rt.setValue(W,"projectionMatrix",A.projectionMatrix),Rt.setValue(W,"viewMatrix",A.matrixWorldInverse);let Tt=Rt.map.cameraPosition;Tt!==void 0&&Tt.setValue(W,St.setFromMatrixPosition(A.matrixWorld)),F.logarithmicDepthBuffer&&Rt.setValue(W,"logDepthBufFC",2/(Math.log(A.far+1)/Math.LN2)),(K.isMeshPhongMaterial||K.isMeshToonMaterial||K.isMeshLambertMaterial||K.isMeshBasicMaterial||K.isMeshStandardMaterial||K.isShaderMaterial)&&Rt.setValue(W,"isOrthographic",A.isOrthographicCamera===!0),V!==A&&(V=A,Gn=!0,Ei=!0)}if(Oe.needsLights&&(rn.state.sunShadowMap.length>0&&Rt.setValue(W,"sunShadowMap",rn.state.sunShadowMap,oe),rn.state.directionalShadowMap.length>0&&Rt.setValue(W,"directionalShadowMap",rn.state.directionalShadowMap,oe),rn.state.spotShadowMap.length>0&&Rt.setValue(W,"spotShadowMap",rn.state.spotShadowMap,oe),rn.state.pointShadowMap.length>0&&Rt.setValue(W,"pointShadowMap",rn.state.pointShadowMap,oe)),Q.isSkinnedMesh){Rt.setOptional(W,Q,"bindMatrix"),Rt.setOptional(W,Q,"bindMatrixInverse");let M=Q.skeleton;M&&(M.boneTexture===null&&M.computeBoneTexture(),Rt.setValue(W,"boneTexture",M.boneTexture,oe))}Q.isBatchedMesh&&(Rt.setOptional(W,Q,"batchingTexture"),Rt.setValue(W,"batchingTexture",Q._matricesTexture,oe),Rt.setOptional(W,Q,"batchingIdTexture"),Rt.setValue(W,"batchingIdTexture",Q._indirectTexture,oe),Rt.setOptional(W,Q,"batchingColorTexture"),Q._colorsTexture!==null&&Rt.setValue(W,"batchingColorTexture",Q._colorsTexture,oe));let Hn=ie.morphAttributes;if((Hn.position!==void 0||Hn.normal!==void 0||Hn.color!==void 0)&&X.update(Q,ie,mn),(Gn||Oe.receiveShadow!==Q.receiveShadow)&&(Oe.receiveShadow=Q.receiveShadow,Rt.setValue(W,"receiveShadow",Q.receiveShadow)),(K.isMeshStandardMaterial||K.isMeshLambertMaterial||K.isMeshPhongMaterial)&&K.envMap===null&&G.environment!==null&&(Wt.envMapIntensity.value=G.environmentIntensity),Wt.dfgLUT!==void 0&&(Wt.dfgLUT.value=Bb()),Gn){if(Rt.setValue(W,"toneMappingExposure",O.toneMappingExposure),Oe.needsLights&&Qr(Wt,Ei),Le&&K.fog===!0&&Xe.refreshFogUniforms(Wt,Le),Xe.refreshMaterialUniforms(Wt,K,fe,le,L.state.transmissionRenderTarget[A.id]),Oe.needsLights&&Oe.lightProbeGrid){let M=Oe.lightProbeGrid;Wt.probesSH.value=M.texture,Wt.probesMin.value.copy(M.boundingBox.min),Wt.probesMax.value.copy(M.boundingBox.max),Wt.probesResolution.value.copy(M.resolution)}Zr.upload(W,Nn(Oe),Wt,oe)}if(K.isShaderMaterial&&K.uniformsNeedUpdate===!0&&(Zr.upload(W,Nn(Oe),Wt,oe),K.uniformsNeedUpdate=!1),K.isSpriteMaterial&&Rt.setValue(W,"center",Q.center),Rt.setValue(W,"modelViewMatrix",Q.modelViewMatrix),Rt.setValue(W,"normalMatrix",Q.normalMatrix),Rt.setValue(W,"modelMatrix",Q.matrixWorld),K.uniformsGroups!==void 0){let M=K.uniformsGroups;for(let Tt=0,wi=M.length;Tt<wi;Tt++){let Wi=M[Tt];me.update(Wi,mn),me.bind(Wi,mn)}}return mn}function Qr(A,G){A.ambientLightColor.needsUpdate=G,A.lightProbe.needsUpdate=G,A.sunLights.needsUpdate=G,A.sunLightShadows.needsUpdate=G,A.directionalLights.needsUpdate=G,A.directionalLightShadows.needsUpdate=G,A.pointLights.needsUpdate=G,A.pointLightShadows.needsUpdate=G,A.spotLights.needsUpdate=G,A.spotLightShadows.needsUpdate=G,A.rectAreaLights.needsUpdate=G,A.hemisphereLights.needsUpdate=G}function _l(A){return A.isMeshLambertMaterial||A.isMeshToonMaterial||A.isMeshPhongMaterial||A.isMeshStandardMaterial||A.isShadowMaterial||A.isShaderMaterial&&A.lights===!0}this.getActiveCubeFace=function(){return k},this.getActiveMipmapLevel=function(){return se},this.getRenderTarget=function(){return _e},this.setRenderTargetTextures=function(A,G,ie){let K=ne.get(A);K.__autoAllocateDepthBuffer=A.resolveDepthBuffer===!1,K.__autoAllocateDepthBuffer===!1&&(K.__useRenderToTexture=!1),ne.get(A.texture).__webglTexture=G,ne.get(A.depthTexture).__webglTexture=K.__autoAllocateDepthBuffer?void 0:ie,K.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(A,G){let ie=ne.get(A);ie.__webglFramebuffer=G,ie.__useDefaultFramebuffer=G===void 0},this.setRenderTarget=function(A,G=0,ie=0){_e=A,k=G,se=ie;let K=null,Q=!1,Le=!1;if(A){let De=ne.get(A);if(De.__useDefaultFramebuffer!==void 0){x.bindFramebuffer(W.FRAMEBUFFER,De.__webglFramebuffer),ge.copy(A.viewport),Ye.copy(A.scissor),$e=A.scissorTest,x.viewport(ge),x.scissor(Ye),x.setScissorTest($e),ae=-1;return}else if(De.__webglFramebuffer===void 0)oe.setupRenderTarget(A);else if(De.__hasExternalTextures)oe.rebindTextures(A,ne.get(A.texture).__webglTexture,ne.get(A.depthTexture).__webglTexture);else if(A.depthBuffer){let lt=A.depthTexture;if(De.__boundDepthTexture!==lt){if(lt!==null&&ne.has(lt)&&(A.width!==lt.image.width||A.height!==lt.image.height))throw new Error("THREE.WebGLRenderer: Attached DepthTexture is initialized to the incorrect size.");oe.setupDepthRenderbuffer(A)}}let Ve=A.texture;(Ve.isData3DTexture||Ve.isDataArrayTexture||Ve.isCompressedArrayTexture)&&(Le=!0);let ze=ne.get(A).__webglFramebuffer;A.isWebGLCubeRenderTarget?(Array.isArray(ze[G])?K=ze[G][ie]:K=ze[G],Q=!0):A.samples>0&&oe.useMultisampledRTT(A)===!1?K=ne.get(A).__webglMultisampledFramebuffer:Array.isArray(ze)?K=ze[ie]:K=ze,ge.copy(A.viewport),Ye.copy(A.scissor),$e=A.scissorTest}else ge.copy(Be).multiplyScalar(fe).floor(),Ye.copy(ut).multiplyScalar(fe).floor(),$e=$t;if(ie!==0&&(K=J),x.bindFramebuffer(W.FRAMEBUFFER,K)&&x.drawBuffers(A,K),x.viewport(ge),x.scissor(Ye),x.setScissorTest($e),Q){let De=ne.get(A.texture);W.framebufferTexture2D(W.FRAMEBUFFER,W.COLOR_ATTACHMENT0,W.TEXTURE_CUBE_MAP_POSITIVE_X+G,De.__webglTexture,ie)}else if(Le){let De=G;for(let Ve=0;Ve<A.textures.length;Ve++){let ze=ne.get(A.textures[Ve]);W.framebufferTextureLayer(W.FRAMEBUFFER,W.COLOR_ATTACHMENT0+Ve,ze.__webglTexture,ie,De)}}else if(A!==null&&ie!==0){let De=ne.get(A.texture);W.framebufferTexture2D(W.FRAMEBUFFER,W.COLOR_ATTACHMENT0,W.TEXTURE_2D,De.__webglTexture,ie)}ae=-1};function qs(A){let G=ne.get(A);return(G.__readFormat!==A.format||G.__readType!==A.type)&&(G.__readFormat=A.format,G.__readType=A.type,G.__formatReadable=F.textureFormatReadable(A.format),G.__typeReadable=F.textureTypeReadable(A.type)),G}this.readRenderTargetPixels=function(A,G,ie,K,Q,Le,be,De=0){if(!(A&&A.isWebGLRenderTarget)){it("WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let Ve=ne.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&be!==void 0&&(Ve=Ve[be]),Ve){x.bindFramebuffer(W.FRAMEBUFFER,Ve);try{let ze=A.textures[De],lt=ze.format,ct=ze.type;A.textures.length>1&&W.readBuffer(W.COLOR_ATTACHMENT0+De);let Ge=qs(ze);if(Ge.__formatReadable===!1){it("WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(Ge.__typeReadable===!1){it("WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}G>=0&&G<=A.width-K&&ie>=0&&ie<=A.height-Q&&W.readPixels(G,ie,K,Q,Pe.convert(lt),Pe.convert(ct),Le)}finally{let ze=_e!==null?ne.get(_e).__webglFramebuffer:null;x.bindFramebuffer(W.FRAMEBUFFER,ze)}}},this.readRenderTargetPixelsAsync=async function(A,G,ie,K,Q,Le,be,De=0){if(!(A&&A.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let Ve=ne.get(A).__webglFramebuffer;if(A.isWebGLCubeRenderTarget&&be!==void 0&&(Ve=Ve[be]),Ve)if(G>=0&&G<=A.width-K&&ie>=0&&ie<=A.height-Q){x.bindFramebuffer(W.FRAMEBUFFER,Ve);let ze=A.textures[De],lt=ze.format,ct=ze.type;A.textures.length>1&&W.readBuffer(W.COLOR_ATTACHMENT0+De);let Ge=qs(ze);if(Ge.__formatReadable===!1)throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(Ge.__typeReadable===!1)throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");let Et=W.createBuffer();W.bindBuffer(W.PIXEL_PACK_BUFFER,Et),W.bufferData(W.PIXEL_PACK_BUFFER,Le.byteLength,W.STREAM_READ),W.readPixels(G,ie,K,Q,Pe.convert(lt),Pe.convert(ct),0),W.bindBuffer(W.PIXEL_PACK_BUFFER,null);let jt=_e!==null?ne.get(_e).__webglFramebuffer:null;x.bindFramebuffer(W.FRAMEBUFFER,jt);let bt=W.fenceSync(W.SYNC_GPU_COMMANDS_COMPLETE,0);return W.flush(),await td(W,bt,4),W.bindBuffer(W.PIXEL_PACK_BUFFER,Et),W.getBufferSubData(W.PIXEL_PACK_BUFFER,0,Le),W.bindBuffer(W.PIXEL_PACK_BUFFER,null),W.deleteBuffer(Et),W.deleteSync(bt),Le}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(A,G=null,ie=0){let K=Math.pow(2,-ie),Q=Math.floor(A.image.width*K),Le=Math.floor(A.image.height*K),be=G!==null?G.x:0,De=G!==null?G.y:0;oe.setTexture2D(A,0),W.copyTexSubImage2D(W.TEXTURE_2D,ie,0,0,be,De,Q,Le),x.unbindTexture()},this.copyTextureToTexture=function(A,G,ie=null,K=null,Q=0,Le=0){let be,De,Ve,ze,lt,ct,Ge,Et,jt,bt=A.isCompressedTexture?A.mipmaps[Le]:A.image;if(ie!==null)be=ie.max.x-ie.min.x,De=ie.max.y-ie.min.y,Ve=ie.isBox3?ie.max.z-ie.min.z:1,ze=ie.min.x,lt=ie.min.y,ct=ie.isBox3?ie.min.z:0;else{let Wt=Math.pow(2,-Q);be=Math.floor(bt.width*Wt),De=Math.floor(bt.height*Wt),A.isDataArrayTexture?Ve=bt.depth:A.isData3DTexture?Ve=Math.floor(bt.depth*Wt):Ve=1,ze=0,lt=0,ct=0}K!==null?(Ge=K.x,Et=K.y,jt=K.z):(Ge=0,Et=0,jt=0);let Pt=Pe.convert(G.format),qe=Pe.convert(G.type),Oe;G.isData3DTexture?(oe.setTexture3D(G,0),Oe=W.TEXTURE_3D):G.isDataArrayTexture||G.isCompressedArrayTexture?(oe.setTexture2DArray(G,0),Oe=W.TEXTURE_2D_ARRAY):(oe.setTexture2D(G,0),Oe=W.TEXTURE_2D),x.activeTexture(W.TEXTURE0),x.pixelStorei(W.UNPACK_FLIP_Y_WEBGL,G.flipY),x.pixelStorei(W.UNPACK_PREMULTIPLY_ALPHA_WEBGL,G.premultiplyAlpha),x.pixelStorei(W.UNPACK_ALIGNMENT,G.unpackAlignment);let rn=x.getParameter(W.UNPACK_ROW_LENGTH),Mt=x.getParameter(W.UNPACK_IMAGE_HEIGHT),mn=x.getParameter(W.UNPACK_SKIP_PIXELS),Un=x.getParameter(W.UNPACK_SKIP_ROWS),Gn=x.getParameter(W.UNPACK_SKIP_IMAGES);x.pixelStorei(W.UNPACK_ROW_LENGTH,bt.width),x.pixelStorei(W.UNPACK_IMAGE_HEIGHT,bt.height),x.pixelStorei(W.UNPACK_SKIP_PIXELS,ze),x.pixelStorei(W.UNPACK_SKIP_ROWS,lt),x.pixelStorei(W.UNPACK_SKIP_IMAGES,ct);let Ei=A.isDataArrayTexture||A.isData3DTexture,Rt=G.isDataArrayTexture||G.isData3DTexture;if(A.isDepthTexture){let Wt=ne.get(A),Hn=ne.get(G),M=ne.get(Wt.__renderTarget),Tt=ne.get(Hn.__renderTarget);x.bindFramebuffer(W.READ_FRAMEBUFFER,M.__webglFramebuffer),x.bindFramebuffer(W.DRAW_FRAMEBUFFER,Tt.__webglFramebuffer);for(let wi=0;wi<Ve;wi++)Ei&&(W.framebufferTextureLayer(W.READ_FRAMEBUFFER,W.COLOR_ATTACHMENT0,ne.get(A).__webglTexture,Q,ct+wi),W.framebufferTextureLayer(W.DRAW_FRAMEBUFFER,W.COLOR_ATTACHMENT0,ne.get(G).__webglTexture,Le,jt+wi)),W.blitFramebuffer(ze,lt,be,De,Ge,Et,be,De,W.DEPTH_BUFFER_BIT,W.NEAREST);x.bindFramebuffer(W.READ_FRAMEBUFFER,null),x.bindFramebuffer(W.DRAW_FRAMEBUFFER,null)}else if(Q!==0||A.isRenderTargetTexture||ne.has(A)){let Wt=ne.get(A),Hn=ne.get(G);x.bindFramebuffer(W.READ_FRAMEBUFFER,H),x.bindFramebuffer(W.DRAW_FRAMEBUFFER,te);for(let M=0;M<Ve;M++)Ei?W.framebufferTextureLayer(W.READ_FRAMEBUFFER,W.COLOR_ATTACHMENT0,Wt.__webglTexture,Q,ct+M):W.framebufferTexture2D(W.READ_FRAMEBUFFER,W.COLOR_ATTACHMENT0,W.TEXTURE_2D,Wt.__webglTexture,Q),Rt?W.framebufferTextureLayer(W.DRAW_FRAMEBUFFER,W.COLOR_ATTACHMENT0,Hn.__webglTexture,Le,jt+M):W.framebufferTexture2D(W.DRAW_FRAMEBUFFER,W.COLOR_ATTACHMENT0,W.TEXTURE_2D,Hn.__webglTexture,Le),Q!==0?W.blitFramebuffer(ze,lt,be,De,Ge,Et,be,De,W.COLOR_BUFFER_BIT,W.NEAREST):Rt?W.copyTexSubImage3D(Oe,Le,Ge,Et,jt+M,ze,lt,be,De):W.copyTexSubImage2D(Oe,Le,Ge,Et,ze,lt,be,De);x.bindFramebuffer(W.READ_FRAMEBUFFER,null),x.bindFramebuffer(W.DRAW_FRAMEBUFFER,null)}else Rt?A.isDataTexture||A.isData3DTexture?W.texSubImage3D(Oe,Le,Ge,Et,jt,be,De,Ve,Pt,qe,bt.data):G.isCompressedArrayTexture?W.compressedTexSubImage3D(Oe,Le,Ge,Et,jt,be,De,Ve,Pt,bt.data):W.texSubImage3D(Oe,Le,Ge,Et,jt,be,De,Ve,Pt,qe,bt):A.isDataTexture?W.texSubImage2D(W.TEXTURE_2D,Le,Ge,Et,be,De,Pt,qe,bt.data):A.isCompressedTexture?W.compressedTexSubImage2D(W.TEXTURE_2D,Le,Ge,Et,bt.width,bt.height,Pt,bt.data):W.texSubImage2D(W.TEXTURE_2D,Le,Ge,Et,be,De,Pt,qe,bt);x.pixelStorei(W.UNPACK_ROW_LENGTH,rn),x.pixelStorei(W.UNPACK_IMAGE_HEIGHT,Mt),x.pixelStorei(W.UNPACK_SKIP_PIXELS,mn),x.pixelStorei(W.UNPACK_SKIP_ROWS,Un),x.pixelStorei(W.UNPACK_SKIP_IMAGES,Gn),Le===0&&G.generateMipmaps&&W.generateMipmap(Oe),x.unbindTexture()},this.initRenderTarget=function(A){ne.get(A).__webglFramebuffer===void 0&&oe.setupRenderTarget(A)},this.initTexture=function(A){A.isCubeTexture?oe.setTextureCube(A,0):A.isData3DTexture?oe.setTexture3D(A,0):A.isDataArrayTexture||A.isCompressedArrayTexture?oe.setTexture2DArray(A,0):oe.setTexture2D(A,0),x.unbindTexture()},this.resetState=function(){k=0,se=0,_e=null,x.reset(),Ne.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return Yn}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(e){this._outputColorSpace=e;let t=this.getContext();t.drawingBufferColorSpace=xt._getDrawingBufferColorSpace(e),t.unpackColorSpace=xt._getUnpackColorSpace()}};var Nd={type:"change"},th={type:"start"},Od={type:"end"},pl=new Di,Ud=new Pn,zb=Math.cos(70*Fc.DEG2RAD),tn=new j,wn=2*Math.PI,Lt={NONE:-1,ROTATE:0,DOLLY:1,PAN:2,TOUCH_ROTATE:3,TOUCH_PAN:4,TOUCH_DOLLY_PAN:5,TOUCH_DOLLY_ROTATE:6},eh=1e-6,ml=class extends Is{constructor(e,t=null){super(e,t),this.state=Lt.NONE,this.target=new j,this.cursor=new j,this.minDistance=0,this.maxDistance=1/0,this.minZoom=0,this.maxZoom=1/0,this.minTargetRadius=0,this.maxTargetRadius=1/0,this.minPolarAngle=0,this.maxPolarAngle=Math.PI,this.minAzimuthAngle=-1/0,this.maxAzimuthAngle=1/0,this.enableDamping=!1,this.dampingFactor=.05,this.enableZoom=!0,this.zoomSpeed=1,this.enableRotate=!0,this.rotateSpeed=1,this.keyRotateSpeed=1,this.enablePan=!0,this.panSpeed=1,this.screenSpacePanning=!0,this.keyPanSpeed=7,this.zoomToCursor=!1,this.autoRotate=!1,this.autoRotateSpeed=2,this.keys={LEFT:"ArrowLeft",UP:"ArrowUp",RIGHT:"ArrowRight",BOTTOM:"ArrowDown"},this.mouseButtons={LEFT:Bi.ROTATE,MIDDLE:Bi.DOLLY,RIGHT:Bi.PAN},this.touches={ONE:ki.ROTATE,TWO:ki.DOLLY_PAN},this.target0=this.target.clone(),this.position0=this.object.position.clone(),this.zoom0=this.object.zoom,this._cursorStyle="auto",this._domElementKeyEvents=null,this._lastPosition=new j,this._lastQuaternion=new In,this._lastTargetPosition=new j,this._quat=new In().setFromUnitVectors(e.up,new j(0,1,0)),this._quatInverse=this._quat.clone().invert(),this._spherical=new Gr,this._sphericalDelta=new Gr,this._scale=1,this._panOffset=new j,this._rotateStart=new nt,this._rotateEnd=new nt,this._rotateDelta=new nt,this._panStart=new nt,this._panEnd=new nt,this._panDelta=new nt,this._dollyStart=new nt,this._dollyEnd=new nt,this._dollyDelta=new nt,this._dollyDirection=new j,this._mouse=new nt,this._performCursorZoom=!1,this._pointers=[],this._pointerPositions={},this._controlActive=!1,this._onPointerMove=Gb.bind(this),this._onPointerDown=Vb.bind(this),this._onPointerUp=Hb.bind(this),this._onContextMenu=Zb.bind(this),this._onMouseWheel=$b.bind(this),this._onKeyDown=jb.bind(this),this._onTouchStart=qb.bind(this),this._onTouchMove=Yb.bind(this),this._onMouseDown=Wb.bind(this),this._onMouseMove=Xb.bind(this),this._interceptControlDown=Jb.bind(this),this._interceptControlUp=Kb.bind(this),this.domElement!==null&&this.connect(this.domElement),this.update()}set cursorStyle(e){this._cursorStyle=e,e==="grab"?this.domElement.style.cursor="grab":this.domElement.style.cursor="auto"}get cursorStyle(){return this._cursorStyle}connect(e){super.connect(e),this.domElement.addEventListener("pointerdown",this._onPointerDown),this.domElement.addEventListener("pointercancel",this._onPointerUp),this.domElement.addEventListener("contextmenu",this._onContextMenu),this.domElement.addEventListener("wheel",this._onMouseWheel,{passive:!1}),this.domElement.getRootNode().addEventListener("keydown",this._interceptControlDown,{passive:!0,capture:!0}),this.domElement.style.touchAction="none"}disconnect(){this.state=Lt.NONE,this.domElement.removeEventListener("pointerdown",this._onPointerDown),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.domElement.removeEventListener("pointercancel",this._onPointerUp),this.domElement.removeEventListener("wheel",this._onMouseWheel),this.domElement.removeEventListener("contextmenu",this._onContextMenu),this.stopListenToKeyEvents();let e=this.domElement.getRootNode();e.removeEventListener("keydown",this._interceptControlDown,{capture:!0}),e.removeEventListener("keyup",this._interceptControlUp,{capture:!0}),this._controlActive=!1,this._pointers.length=0,this._pointerPositions={},this.domElement.style.touchAction="",this.domElement.style.cursor="auto"}dispose(){this.disconnect()}getPolarAngle(){return this._spherical.phi}getAzimuthalAngle(){return this._spherical.theta}getDistance(){return this.object.position.distanceTo(this.target)}listenToKeyEvents(e){e.addEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=e}stopListenToKeyEvents(){this._domElementKeyEvents!==null&&(this._domElementKeyEvents.removeEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=null)}saveState(){this.target0.copy(this.target),this.position0.copy(this.object.position),this.zoom0=this.object.zoom}reset(){this.target.copy(this.target0),this.object.position.copy(this.position0),this.object.zoom=this.zoom0,this.object.updateProjectionMatrix(),this.dispatchEvent(Nd),this.update(),this.state=Lt.NONE}pan(e,t){this._pan(e,t),this.update()}dollyIn(e){this._dollyIn(e),this.update()}dollyOut(e){this._dollyOut(e),this.update()}rotateLeft(e){this._rotateLeft(e),this.update()}rotateUp(e){this._rotateUp(e),this.update()}update(e=null){let t=this.object.position;tn.copy(t).sub(this.target),tn.applyQuaternion(this._quat),this._spherical.setFromVector3(tn),this.autoRotate&&this.state===Lt.NONE&&this._rotateLeft(this._getAutoRotationAngle(e)),this.enableDamping?(this._spherical.theta+=this._sphericalDelta.theta*this.dampingFactor,this._spherical.phi+=this._sphericalDelta.phi*this.dampingFactor):(this._spherical.theta+=this._sphericalDelta.theta,this._spherical.phi+=this._sphericalDelta.phi);let n=this.minAzimuthAngle,s=this.maxAzimuthAngle;isFinite(n)&&isFinite(s)&&(n<-Math.PI?n+=wn:n>Math.PI&&(n-=wn),s<-Math.PI?s+=wn:s>Math.PI&&(s-=wn),n<=s?this._spherical.theta=Math.max(n,Math.min(s,this._spherical.theta)):this._spherical.theta=this._spherical.theta>(n+s)/2?Math.max(n,this._spherical.theta):Math.min(s,this._spherical.theta)),this._spherical.phi=Math.max(this.minPolarAngle,Math.min(this.maxPolarAngle,this._spherical.phi)),this._spherical.makeSafe(),this.enableDamping===!0?this.target.addScaledVector(this._panOffset,this.dampingFactor):this.target.add(this._panOffset),this.target.sub(this.cursor),this.target.clampLength(this.minTargetRadius,this.maxTargetRadius),this.target.add(this.cursor);let o=!1;if(this.zoomToCursor&&this._performCursorZoom||this.object.isOrthographicCamera)this._spherical.radius=this._clampDistance(this._spherical.radius);else{let l=this._spherical.radius;this._spherical.radius=this._clampDistance(this._spherical.radius*this._scale),o=l!=this._spherical.radius}if(tn.setFromSpherical(this._spherical),tn.applyQuaternion(this._quatInverse),t.copy(this.target).add(tn),this.object.lookAt(this.target),this.enableDamping===!0?(this._sphericalDelta.theta*=1-this.dampingFactor,this._sphericalDelta.phi*=1-this.dampingFactor,this._panOffset.multiplyScalar(1-this.dampingFactor)):(this._sphericalDelta.set(0,0,0),this._panOffset.set(0,0,0)),this.zoomToCursor&&this._performCursorZoom){let l=null;if(this.object.isPerspectiveCamera){let h=tn.length();l=this._clampDistance(h*this._scale);let d=h-l;this.object.position.addScaledVector(this._dollyDirection,d),this.object.updateMatrixWorld(),o=!!d}else if(this.object.isOrthographicCamera){let h=new j(this._mouse.x,this._mouse.y,0);h.unproject(this.object);let d=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),this.object.updateProjectionMatrix(),o=d!==this.object.zoom;let f=new j(this._mouse.x,this._mouse.y,0);f.unproject(this.object),this.object.position.sub(f).add(h),this.object.updateMatrixWorld(),l=tn.length()}else console.warn("WARNING: OrbitControls.js encountered an unknown camera type - zoom to cursor disabled."),this.zoomToCursor=!1;l!==null&&(this.screenSpacePanning?this.target.set(0,0,-1).transformDirection(this.object.matrix).multiplyScalar(l).add(this.object.position):(pl.origin.copy(this.object.position),pl.direction.set(0,0,-1).transformDirection(this.object.matrix),Math.abs(this.object.up.dot(pl.direction))<zb?this.object.lookAt(this.target):(Ud.setFromNormalAndCoplanarPoint(this.object.up,this.target),pl.intersectPlane(Ud,this.target))))}else if(this.object.isOrthographicCamera){let l=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),l!==this.object.zoom&&(this.object.updateProjectionMatrix(),o=!0)}return this._scale=1,this._performCursorZoom=!1,o||this._lastPosition.distanceToSquared(this.object.position)>eh||8*(1-this._lastQuaternion.dot(this.object.quaternion))>eh||this._lastTargetPosition.distanceToSquared(this.target)>eh?(this.dispatchEvent(Nd),this._lastPosition.copy(this.object.position),this._lastQuaternion.copy(this.object.quaternion),this._lastTargetPosition.copy(this.target),!0):!1}_getAutoRotationAngle(e){return e!==null?wn/60*this.autoRotateSpeed*e:wn/60/60*this.autoRotateSpeed}_getZoomScale(e){let t=Math.abs(e*.01);return Math.pow(.95,this.zoomSpeed*t)}_rotateLeft(e){this._sphericalDelta.theta-=e}_rotateUp(e){this._sphericalDelta.phi-=e}_panLeft(e,t){tn.setFromMatrixColumn(t,0),tn.multiplyScalar(-e),this._panOffset.add(tn)}_panUp(e,t){this.screenSpacePanning===!0?tn.setFromMatrixColumn(t,1):(tn.setFromMatrixColumn(t,0),tn.crossVectors(this.object.up,tn)),tn.multiplyScalar(e),this._panOffset.add(tn)}_pan(e,t){let n=this.domElement;if(this.object.isPerspectiveCamera){let s=this.object.position;tn.copy(s).sub(this.target);let o=tn.length();o*=Math.tan(this.object.fov/2*Math.PI/180),this._panLeft(2*e*o/n.clientHeight,this.object.matrix),this._panUp(2*t*o/n.clientHeight,this.object.matrix)}else this.object.isOrthographicCamera?(this._panLeft(e*(this.object.right-this.object.left)/this.object.zoom/n.clientWidth,this.object.matrix),this._panUp(t*(this.object.top-this.object.bottom)/this.object.zoom/n.clientHeight,this.object.matrix)):(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - pan disabled."),this.enablePan=!1)}_dollyOut(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale/=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_dollyIn(e){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale*=e:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_updateZoomParameters(e,t){if(!this.zoomToCursor)return;this._performCursorZoom=!0;let n=this.domElement.getBoundingClientRect(),s=e-n.left,o=t-n.top,l=n.width,h=n.height;this._mouse.x=s/l*2-1,this._mouse.y=-(o/h)*2+1,this._dollyDirection.set(this._mouse.x,this._mouse.y,1).unproject(this.object).sub(this.object.position).normalize()}_clampDistance(e){return Math.max(this.minDistance,Math.min(this.maxDistance,e))}_handleMouseDownRotate(e){this._rotateStart.set(e.clientX,e.clientY)}_handleMouseDownDolly(e){this._updateZoomParameters(e.clientX,e.clientX),this._dollyStart.set(e.clientX,e.clientY)}_handleMouseDownPan(e){this._panStart.set(e.clientX,e.clientY)}_handleMouseMoveRotate(e){this._rotateEnd.set(e.clientX,e.clientY),this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(wn*this._rotateDelta.x/t.clientHeight),this._rotateUp(wn*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd),this.update()}_handleMouseMoveDolly(e){this._dollyEnd.set(e.clientX,e.clientY),this._dollyDelta.subVectors(this._dollyEnd,this._dollyStart),this._dollyDelta.y>0?this._dollyOut(this._getZoomScale(this._dollyDelta.y)):this._dollyDelta.y<0&&this._dollyIn(this._getZoomScale(this._dollyDelta.y)),this._dollyStart.copy(this._dollyEnd),this.update()}_handleMouseMovePan(e){this._panEnd.set(e.clientX,e.clientY),this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd),this.update()}_handleMouseWheel(e){this._updateZoomParameters(e.clientX,e.clientY),e.deltaY<0?this._dollyIn(this._getZoomScale(e.deltaY)):e.deltaY>0&&this._dollyOut(this._getZoomScale(e.deltaY)),this.update()}_handleKeyDown(e){let t=!1;switch(e.code){case this.keys.UP:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(wn*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,this.keyPanSpeed),t=!0;break;case this.keys.BOTTOM:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateUp(-wn*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,-this.keyPanSpeed),t=!0;break;case this.keys.LEFT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(wn*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(this.keyPanSpeed,0),t=!0;break;case this.keys.RIGHT:e.ctrlKey||e.metaKey||e.shiftKey?this.enableRotate&&this._rotateLeft(-wn*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(-this.keyPanSpeed,0),t=!0;break}t&&(e.preventDefault(),this.update())}_handleTouchStartRotate(e){if(this._pointers.length===1)this._rotateStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),n=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._rotateStart.set(n,s)}}_handleTouchStartPan(e){if(this._pointers.length===1)this._panStart.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),n=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._panStart.set(n,s)}}_handleTouchStartDolly(e){let t=this._getSecondPointerPosition(e),n=e.pageX-t.x,s=e.pageY-t.y,o=Math.sqrt(n*n+s*s);this._dollyStart.set(0,o)}_handleTouchStartDollyPan(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enablePan&&this._handleTouchStartPan(e)}_handleTouchStartDollyRotate(e){this.enableZoom&&this._handleTouchStartDolly(e),this.enableRotate&&this._handleTouchStartRotate(e)}_handleTouchMoveRotate(e){if(this._pointers.length==1)this._rotateEnd.set(e.pageX,e.pageY);else{let n=this._getSecondPointerPosition(e),s=.5*(e.pageX+n.x),o=.5*(e.pageY+n.y);this._rotateEnd.set(s,o)}this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let t=this.domElement;this._rotateLeft(wn*this._rotateDelta.x/t.clientHeight),this._rotateUp(wn*this._rotateDelta.y/t.clientHeight),this._rotateStart.copy(this._rotateEnd)}_handleTouchMovePan(e){if(this._pointers.length===1)this._panEnd.set(e.pageX,e.pageY);else{let t=this._getSecondPointerPosition(e),n=.5*(e.pageX+t.x),s=.5*(e.pageY+t.y);this._panEnd.set(n,s)}this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd)}_handleTouchMoveDolly(e){let t=this._getSecondPointerPosition(e),n=e.pageX-t.x,s=e.pageY-t.y,o=Math.sqrt(n*n+s*s);this._dollyEnd.set(0,o),this._dollyDelta.set(0,Math.pow(this._dollyEnd.y/this._dollyStart.y,this.zoomSpeed)),this._dollyOut(this._dollyDelta.y),this._dollyStart.copy(this._dollyEnd);let l=(e.pageX+t.x)*.5,h=(e.pageY+t.y)*.5;this._updateZoomParameters(l,h)}_handleTouchMoveDollyPan(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enablePan&&this._handleTouchMovePan(e)}_handleTouchMoveDollyRotate(e){this.enableZoom&&this._handleTouchMoveDolly(e),this.enableRotate&&this._handleTouchMoveRotate(e)}_addPointer(e){this._pointers.push(e.pointerId)}_removePointer(e){delete this._pointerPositions[e.pointerId];for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId){this._pointers.splice(t,1);return}}_isTrackingPointer(e){for(let t=0;t<this._pointers.length;t++)if(this._pointers[t]==e.pointerId)return!0;return!1}_trackPointer(e){let t=this._pointerPositions[e.pointerId];t===void 0&&(t=new nt,this._pointerPositions[e.pointerId]=t),t.set(e.pageX,e.pageY)}_getSecondPointerPosition(e){let t=e.pointerId===this._pointers[0]?this._pointers[1]:this._pointers[0];return this._pointerPositions[t]}_customWheelEvent(e){let t=e.deltaMode,n={clientX:e.clientX,clientY:e.clientY,deltaY:e.deltaY};switch(t){case 1:n.deltaY*=16;break;case 2:n.deltaY*=100;break}return e.ctrlKey&&!this._controlActive&&(n.deltaY*=10),n}};function Vb(i){this.enabled!==!1&&(this._pointers.length===0&&(this.domElement.setPointerCapture(i.pointerId),this.domElement.ownerDocument.addEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.addEventListener("pointerup",this._onPointerUp)),!this._isTrackingPointer(i)&&(this._addPointer(i),i.pointerType==="touch"?this._onTouchStart(i):this._onMouseDown(i),this._cursorStyle==="grab"&&(this.domElement.style.cursor="grabbing")))}function Gb(i){this.enabled!==!1&&(i.pointerType==="touch"?this._onTouchMove(i):this._onMouseMove(i))}function Hb(i){switch(this._removePointer(i),this._pointers.length){case 0:this.domElement.releasePointerCapture(i.pointerId),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.dispatchEvent(Od),this.state=Lt.NONE,this._cursorStyle==="grab"&&(this.domElement.style.cursor="grab");break;case 1:let e=this._pointers[0],t=this._pointerPositions[e];this._onTouchStart({pointerId:e,pageX:t.x,pageY:t.y});break}}function Wb(i){let e;switch(i.button){case 0:e=this.mouseButtons.LEFT;break;case 1:e=this.mouseButtons.MIDDLE;break;case 2:e=this.mouseButtons.RIGHT;break;default:e=-1}switch(e){case Bi.DOLLY:if(this.enableZoom===!1)return;this._handleMouseDownDolly(i),this.state=Lt.DOLLY;break;case Bi.ROTATE:if(i.ctrlKey||i.metaKey||i.shiftKey){if(this.enablePan===!1)return;this._handleMouseDownPan(i),this.state=Lt.PAN}else{if(this.enableRotate===!1)return;this._handleMouseDownRotate(i),this.state=Lt.ROTATE}break;case Bi.PAN:if(i.ctrlKey||i.metaKey||i.shiftKey){if(this.enableRotate===!1)return;this._handleMouseDownRotate(i),this.state=Lt.ROTATE}else{if(this.enablePan===!1)return;this._handleMouseDownPan(i),this.state=Lt.PAN}break;default:this.state=Lt.NONE}this.state!==Lt.NONE&&this.dispatchEvent(th)}function Xb(i){switch(this.state){case Lt.ROTATE:if(this.enableRotate===!1)return;this._handleMouseMoveRotate(i);break;case Lt.DOLLY:if(this.enableZoom===!1)return;this._handleMouseMoveDolly(i);break;case Lt.PAN:if(this.enablePan===!1)return;this._handleMouseMovePan(i);break}}function $b(i){this.enabled===!1||this.enableZoom===!1||this.state!==Lt.NONE||(i.preventDefault(),this.dispatchEvent(th),this._handleMouseWheel(this._customWheelEvent(i)),this.dispatchEvent(Od))}function jb(i){this.enabled!==!1&&this._handleKeyDown(i)}function qb(i){switch(this._trackPointer(i),this._pointers.length){case 1:switch(this.touches.ONE){case ki.ROTATE:if(this.enableRotate===!1)return;this._handleTouchStartRotate(i),this.state=Lt.TOUCH_ROTATE;break;case ki.PAN:if(this.enablePan===!1)return;this._handleTouchStartPan(i),this.state=Lt.TOUCH_PAN;break;default:this.state=Lt.NONE}break;case 2:switch(this.touches.TWO){case ki.DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchStartDollyPan(i),this.state=Lt.TOUCH_DOLLY_PAN;break;case ki.DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchStartDollyRotate(i),this.state=Lt.TOUCH_DOLLY_ROTATE;break;default:this.state=Lt.NONE}break;default:this.state=Lt.NONE}this.state!==Lt.NONE&&this.dispatchEvent(th)}function Yb(i){switch(this._trackPointer(i),this.state){case Lt.TOUCH_ROTATE:if(this.enableRotate===!1)return;this._handleTouchMoveRotate(i),this.update();break;case Lt.TOUCH_PAN:if(this.enablePan===!1)return;this._handleTouchMovePan(i),this.update();break;case Lt.TOUCH_DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchMoveDollyPan(i),this.update();break;case Lt.TOUCH_DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchMoveDollyRotate(i),this.update();break;default:this.state=Lt.NONE}}function Zb(i){this.enabled!==!1&&i.preventDefault()}function Jb(i){i.key==="Control"&&(this._controlActive=!0,this.domElement.getRootNode().addEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}function Kb(i){i.key==="Control"&&(this._controlActive=!1,this.domElement.getRootNode().removeEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}var Qb=(async function(i={}){var e,t=i,n=typeof window=="object",s=typeof WorkerGlobalScope<"u",o=typeof process=="object"&&process.versions?.node&&process.type!="renderer",l=!n&&!o&&!s;if(o){let{createRequire:r}=await import("module");var h=r(import.meta.url)}var d=[],f="./this.program",g=(r,a)=>{throw a},y=import.meta.url,m="";function S(r){return t.locateFile?t.locateFile(r,m):m+r}var T,P;if(o){if(!(typeof process=="object"&&process.versions?.node&&process.type!="renderer"))throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)");var b=process.versions.node,_=b.split(".").slice(0,3);if(_=_[0]*1e4+_[1]*100+_[2].split("-")[0]*1,_<16e4)throw new Error("This emscripten-generated code requires node v16.0.0 (detected v"+b+")");var U=h("fs");y.startsWith("file:")&&(m=h("path").dirname(h("url").fileURLToPath(y))+"/"),P=a=>{a=se(a)?new URL(a):a;var c=U.readFileSync(a);return k(Buffer.isBuffer(c)),c},T=async(a,c=!0)=>{a=se(a)?new URL(a):a;var u=U.readFileSync(a,c?void 0:"utf8");return k(c?Buffer.isBuffer(u):typeof u=="string"),u},process.argv.length>1&&(f=process.argv[1].replace(/\\/g,"/")),d=process.argv.slice(2),g=(a,c)=>{throw process.exitCode=a,c}}else if(l){if(typeof process=="object"&&process.versions?.node&&process.type!="renderer"||typeof window=="object"||typeof WorkerGlobalScope<"u")throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)")}else if(n||s){try{m=new URL(".",y).href}catch{}if(!(typeof window=="object"||typeof WorkerGlobalScope<"u"))throw new Error("not compiled for this environment (did you build to HTML and try to run it not on the web, or set ENVIRONMENT to something - like node - and run it someplace else - like on the web?)");s&&(P=r=>{var a=new XMLHttpRequest;return a.open("GET",r,!1),a.responseType="arraybuffer",a.send(null),new Uint8Array(a.response)}),T=async r=>{if(se(r))return new Promise((c,u)=>{var p=new XMLHttpRequest;p.open("GET",r,!0),p.responseType="arraybuffer",p.onload=()=>{if(p.status==200||p.status==0&&p.response){c(p.response);return}u(p.status)},p.onerror=u,p.send(null)});var a=await fetch(r,{credentials:"same-origin"});if(a.ok)return a.arrayBuffer();throw new Error(a.status+" : "+a.url)}}else throw new Error("environment detection error");var z=console.log.bind(console),R=console.error.bind(console),I="IDBFS is no longer included by default; build with -lidbfs.js",L="PROXYFS is no longer included by default; build with -lproxyfs.js",B="WORKERFS is no longer included by default; build with -lworkerfs.js",w="FETCHFS is no longer included by default; build with -lfetchfs.js",D="ICASEFS is no longer included by default; build with -licasefs.js",O="JSFILEFS is no longer included by default; build with -ljsfilefs.js",q="OPFS is no longer included by default; build with -lopfs.js",Y="NODEFS is no longer included by default; build with -lnodefs.js";k(!l,"shell environment detected but not enabled at build time.  Add `shell` to `-sENVIRONMENT` to enable.");var J;typeof WebAssembly!="object"&&R("no native wasm support detected");var H=!1,te;function k(r,a){r||xe("Assertion failed"+(a?": "+a:""))}var se=r=>r.startsWith("file://");function _e(){var r=Pl();k((r&3)==0),r==0&&(r+=4),Ue[r>>2]=34821223,Ue[r+4>>2]=2310721022,Ue[0]=1668509029}function ae(){if(!H){var r=Pl();r==0&&(r+=4);var a=Ue[r>>2],c=Ue[r+4>>2];(a!=34821223||c!=2310721022)&&xe(`Stack overflow! Stack cookie has been overwritten at ${Mi(r)}, expected hex dwords 0x89BACDFE and 0x2135467, but received ${Mi(c)} ${Mi(a)}`),Ue[0]!=1668509029&&xe("Runtime error: The application has corrupted its heap memory area (address zero)!")}}class V extends Error{}class ge extends V{}class Ye extends V{constructor(a){super(a),this.excPtr=a;let c=Rh(a);this.name=c[0],this.message=c[1]}}var $e=!0;function Ut(...r){!$e&&typeof $e<"u"||console.warn(...r)}(()=>{var r=new Int16Array(1),a=new Int8Array(r.buffer);if(r[0]=25459,a[0]!==115||a[1]!==99)throw"Runtime error: expected the system to be little-endian! (Run with -sSUPPORT_BIG_ENDIAN to bypass)"})();function mt(r){Object.getOwnPropertyDescriptor(t,r)||Object.defineProperty(t,r,{configurable:!0,set(){xe(`Attempt to set \`Module.${r}\` after it has already been processed.  This can happen, for example, when code is injected via '--post-js' rather than '--pre-js'`)}})}function Ke(r){return()=>k(!1,`call to '${r}' via reference taken before Wasm module initialization`)}function le(r){Object.getOwnPropertyDescriptor(t,r)&&xe(`\`Module.${r}\` was supplied but \`${r}\` not included in INCOMING_MODULE_JS_API`)}function fe(r){return r==="FS_createPath"||r==="FS_createDataFile"||r==="FS_createPreloadedFile"||r==="FS_unlink"||r==="addRunDependency"||r==="FS_createLazyFile"||r==="FS_createDevice"||r==="removeRunDependency"}function ke(r,a){typeof globalThis<"u"&&!Object.getOwnPropertyDescriptor(globalThis,r)&&Object.defineProperty(globalThis,r,{configurable:!0,get(){a()}})}function st(r,a){ke(r,()=>{Vn(`\`${r}\` is not longer defined by emscripten. ${a}`)})}st("buffer","Please use HEAP8.buffer or wasmMemory.buffer"),st("asm","Please use wasmExports instead");function Be(r){ke(r,()=>{var a=`\`${r}\` is a library symbol and not included by default; add it to your library.js __deps or to DEFAULT_LIBRARY_FUNCS_TO_INCLUDE on the command line`,c=r;c.startsWith("_")||(c="$"+r),a+=` (e.g. -sDEFAULT_LIBRARY_FUNCS_TO_INCLUDE='${c}')`,fe(r)&&(a+=". Alternatively, forcing filesystem support (-sFORCE_FILESYSTEM) can export this for you"),Vn(a)}),ut(r)}function ut(r){Object.getOwnPropertyDescriptor(t,r)||Object.defineProperty(t,r,{configurable:!0,get(){var a=`'${r}' was not exported. add it to EXPORTED_RUNTIME_METHODS (see the Emscripten FAQ)`;fe(r)&&(a+=". Alternatively, forcing filesystem support (-sFORCE_FILESYSTEM) can export this for you"),xe(a)}})}var $t,dt,gt,rt,tt,St,Bt,Ie,Ue,Vt,W,Dt,Ct,F=!1;function x(){var r=gt.buffer;rt=new Int8Array(r),St=new Int16Array(r),tt=new Uint8Array(r),Bt=new Uint16Array(r),Ie=new Int32Array(r),Ue=new Uint32Array(r),Vt=new Float32Array(r),W=new Float64Array(r),Dt=new BigInt64Array(r),Ct=new BigUint64Array(r)}k(typeof Int32Array<"u"&&typeof Float64Array<"u"&&Int32Array.prototype.subarray!=null&&Int32Array.prototype.set!=null,"JS engine does not provide full typed array support");function Z(){if(t.preRun)for(typeof t.preRun=="function"&&(t.preRun=[t.preRun]);t.preRun.length;)Tn(t.preRun.shift());mt("preRun"),je(wt)}function ne(){k(!F),F=!0,ae(),!t.noFSInit&&!M.initialized&&M.init(),bt.init(),Yi.__wasm_call_ctors(),M.ignorePermissions=!1}function oe(){if(ae(),t.postRun)for(typeof t.postRun=="function"&&(t.postRun=[t.postRun]);t.postRun.length;)Ft(t.postRun.shift());mt("postRun"),je(We)}var Ee=0,Ae=null,re={},he=null;function Ce(r){Ee++,t.monitorRunDependencies?.(Ee),r?(k(!re[r]),re[r]=1,he===null&&typeof setInterval<"u"&&(he=setInterval(()=>{if(H){clearInterval(he),he=null;return}var a=!1;for(var c in re)a||(a=!0,R("still waiting on run dependencies:")),R(`dependency: ${c}`);a&&R("(end of list)")},1e4))):R("warning: run dependency added without ID")}function Xe(r){if(Ee--,t.monitorRunDependencies?.(Ee),r?(k(re[r]),delete re[r]):R("warning: run dependency removed without ID"),Ee==0&&(he!==null&&(clearInterval(he),he=null),Ae)){var a=Ae;Ae=null,a()}}function xe(r){t.onAbort?.(r),r="Aborted("+r+")",R(r),H=!0;var a=new WebAssembly.RuntimeError(r);throw dt?.(a),a}function Te(r,a){return(...c)=>{k(F,`native function \`${r}\` called before runtime initialization`);var u=Yi[r];return k(u,`exported native function \`${r}\` not found`),k(c.length<=a,`native function \`${r}\` called with ${c.length} args but expects ${a}`),u(...c)}}var He;function Je(){return t.locateFile?S("mujoco.wasm"):new URL("mujoco.wasm",import.meta.url).href}function ot(r){if(r==He&&J)return new Uint8Array(J);if(P)return P(r);throw"both async and sync fetching of the wasm failed"}async function X(r){if(!J)try{var a=await T(r);return new Uint8Array(a)}catch{}return ot(r)}async function Re(r,a){try{var c=await X(r),u=await WebAssembly.instantiate(c,a);return u}catch(p){R(`failed to asynchronously prepare wasm: ${p}`),se(He)&&R(`warning: Loading from a file URI (${He}) is not supported in most browsers. See https://emscripten.org/docs/getting_started/FAQ.html#how-do-i-run-a-local-webserver-for-testing-why-does-my-program-stall-in-downloading-or-preparing`),xe(p)}}async function de(r,a,c){if(!r&&typeof WebAssembly.instantiateStreaming=="function"&&!se(a)&&!o)try{var u=fetch(a,{credentials:"same-origin"}),p=await WebAssembly.instantiateStreaming(u,c);return p}catch(v){R(`wasm streaming compile failed: ${v}`),R("falling back to ArrayBuffer instantiation")}return Re(a,c)}function Pe(){return{env:Vh,wasi_snapshot_preview1:Vh}}async function Ne(){function r(E,C){return Yi=E.exports,gt=Yi.memory,k(gt,"memory not found in wasm exports"),x(),ra=Yi.__indirect_function_table,k(ra,"table not found in wasm exports"),im(Yi),Xe("wasm-instantiate"),Yi}Ce("wasm-instantiate");var a=t;function c(E){return k(t===a,"the Module object should not be replaced during async compilation - perhaps the order of HTML elements is wrong?"),a=null,r(E.instance)}var u=Pe();if(t.instantiateWasm)return new Promise((E,C)=>{try{t.instantiateWasm(u,(N,$)=>{E(r(N,$))})}catch(N){R(`Module.instantiateWasm callback failed with error: ${N}`),C(N)}});He??=Je();var p=await de(J,He,u),v=c(p);return v}class me{name="ExitStatus";constructor(a){this.message=`Program terminated with exit(${a})`,this.status=a}}var je=r=>{for(;r.length>0;)r.shift()(t)},We=[],Ft=r=>We.push(r),wt=[],Tn=r=>wt.push(r);function zn(r,a="i8"){switch(a.endsWith("*")&&(a="*"),a){case"i1":return rt[r];case"i8":return rt[r];case"i16":return St[r>>1];case"i32":return Ie[r>>2];case"i64":return Dt[r>>3];case"float":return Vt[r>>2];case"double":return W[r>>3];case"*":return Ue[r>>2];default:xe(`invalid type for getValue: ${a}`)}}var Ws=!0,Mi=r=>(k(typeof r=="number"),r>>>=0,"0x"+r.toString(16).padStart(8,"0"));function gl(r,a,c="i8"){switch(c.endsWith("*")&&(c="*"),c){case"i1":rt[r]=a;break;case"i8":rt[r]=a;break;case"i16":St[r>>1]=a;break;case"i32":Ie[r>>2]=a;break;case"i64":Dt[r>>3]=BigInt(a);break;case"float":Vt[r>>2]=a;break;case"double":W[r>>3]=a;break;case"*":Ue[r>>2]=a;break;default:xe(`invalid type for setValue: ${c}`)}}var ye=r=>Nh(r),Se=()=>Oh(),Vn=r=>{Vn.shown||={},Vn.shown[r]||(Vn.shown[r]=1,o&&(r="warning: "+r),R(r))},Kr=typeof TextDecoder<"u"?new TextDecoder:void 0,Sn=(r,a=0,c=NaN)=>{for(var u=a+c,p=a;r[p]&&!(p>=u);)++p;if(p-a>16&&r.buffer&&Kr)return Kr.decode(r.subarray(a,p));for(var v="";a<p;){var E=r[a++];if(!(E&128)){v+=String.fromCharCode(E);continue}var C=r[a++]&63;if((E&224)==192){v+=String.fromCharCode((E&31)<<6|C);continue}var N=r[a++]&63;if((E&240)==224?E=(E&15)<<12|C<<6|N:((E&248)!=240&&Vn("Invalid UTF-8 leading byte "+Mi(E)+" encountered when deserializing a UTF-8 string in wasm memory to a JS string!"),E=(E&7)<<18|C<<12|N<<6|r[a++]&63),E<65536)v+=String.fromCharCode(E);else{var $=E-65536;v+=String.fromCharCode(55296|$>>10,56320|$&1023)}}return v},An=(r,a)=>(k(typeof r=="number",`UTF8ToString expects a number (got ${typeof r})`),r?Sn(tt,r,a):""),Xs=(r,a,c,u)=>xe(`Assertion failed: ${An(r)}, at: `+[a?An(a):"unknown filename",c,u?An(u):"unknown function"]),Fn=[],fi=0,$s=r=>{var a=new ur(r);return a.get_caught()||(a.set_caught(!0),fi--),a.set_rethrown(!1),Fn.push(a),ua(r),zh(r)},hr=()=>{if(!Fn.length)return 0;var r=Fn[Fn.length-1];return ua(r.excPtr),r.excPtr},Nn=0,js=()=>{Me(0,0),k(Fn.length>0);var r=Fn.pop();Il(r.excPtr),Nn=0};class ur{constructor(a){this.excPtr=a,this.ptr=a-24}set_type(a){Ue[this.ptr+4>>2]=a}get_type(){return Ue[this.ptr+4>>2]}set_destructor(a){Ue[this.ptr+8>>2]=a}get_destructor(){return Ue[this.ptr+8>>2]}set_caught(a){a=a?1:0,rt[this.ptr+12]=a}get_caught(){return rt[this.ptr+12]!=0}set_rethrown(a){a=a?1:0,rt[this.ptr+13]=a}get_rethrown(){return rt[this.ptr+13]!=0}init(a,c){this.set_adjusted_ptr(0),this.set_type(a),this.set_destructor(c)}set_adjusted_ptr(a){Ue[this.ptr+16>>2]=a}get_adjusted_ptr(){return Ue[this.ptr+16>>2]}}var dr=r=>Lh(r),Qr=r=>{var a=Nn?.excPtr;if(!a)return dr(0),0;var c=new ur(a);c.set_adjusted_ptr(a);var u=c.get_type();if(!u)return dr(0),a;for(var p of r){if(p===0||p===u)break;var v=c.ptr+16;if(kh(p,u,v))return dr(p),a}return dr(u),a},_l=()=>Qr([]),qs=r=>Qr([r]),A=(r,a)=>Qr([r,a]),G=()=>{var r=Fn.pop();r||xe("no exception to throw");var a=r.excPtr;throw r.get_rethrown()||(Fn.push(r),r.set_rethrown(!0),r.set_caught(!1),fi++),Nn=new Ye(a),Nn},ie=r=>{if(r){var a=new ur(r);Fn.push(a),a.set_rethrown(!0),G()}},K=(r,a,c)=>{var u=new ur(r);throw u.init(a,c),Nn=new Ye(r),fi++,Nn},Q=()=>fi,Le=r=>{throw Nn||(Nn=new Ye(r)),Nn},be={isAbs:r=>r.charAt(0)==="/",splitPath:r=>{var a=/^(\/?|)([\s\S]*?)((?:\.{1,2}|[^\/]+?|)(\.[^.\/]*|))(?:[\/]*)$/;return a.exec(r).slice(1)},normalizeArray:(r,a)=>{for(var c=0,u=r.length-1;u>=0;u--){var p=r[u];p==="."?r.splice(u,1):p===".."?(r.splice(u,1),c++):c&&(r.splice(u,1),c--)}if(a)for(;c;c--)r.unshift("..");return r},normalize:r=>{var a=be.isAbs(r),c=r.slice(-1)==="/";return r=be.normalizeArray(r.split("/").filter(u=>!!u),!a).join("/"),!r&&!a&&(r="."),r&&c&&(r+="/"),(a?"/":"")+r},dirname:r=>{var a=be.splitPath(r),c=a[0],u=a[1];return!c&&!u?".":(u&&(u=u.slice(0,-1)),c+u)},basename:r=>r&&r.match(/([^\/]+|\/)\/*$/)[1],join:(...r)=>be.normalize(r.join("/")),join2:(r,a)=>be.normalize(r+"/"+a)},De=()=>{if(o){var r=h("crypto");return a=>r.randomFillSync(a)}return a=>crypto.getRandomValues(a)},Ve=r=>{(Ve=De())(r)},ze={resolve:(...r)=>{for(var a="",c=!1,u=r.length-1;u>=-1&&!c;u--){var p=u>=0?r[u]:M.cwd();if(typeof p!="string")throw new TypeError("Arguments to path.resolve must be strings");if(!p)return"";a=p+"/"+a,c=be.isAbs(p)}return a=be.normalizeArray(a.split("/").filter(v=>!!v),!c).join("/"),(c?"/":"")+a||"."},relative:(r,a)=>{r=ze.resolve(r).slice(1),a=ze.resolve(a).slice(1);function c($){for(var ee=0;ee<$.length&&$[ee]==="";ee++);for(var ue=$.length-1;ue>=0&&$[ue]==="";ue--);return ee>ue?[]:$.slice(ee,ue-ee+1)}for(var u=c(r.split("/")),p=c(a.split("/")),v=Math.min(u.length,p.length),E=v,C=0;C<v;C++)if(u[C]!==p[C]){E=C;break}for(var N=[],C=E;C<u.length;C++)N.push("..");return N=N.concat(p.slice(E)),N.join("/")}},lt=[],ct=r=>{for(var a=0,c=0;c<r.length;++c){var u=r.charCodeAt(c);u<=127?a++:u<=2047?a+=2:u>=55296&&u<=57343?(a+=4,++c):a+=3}return a},Ge=(r,a,c,u)=>{if(k(typeof r=="string",`stringToUTF8Array expects a string (got ${typeof r})`),!(u>0))return 0;for(var p=c,v=c+u-1,E=0;E<r.length;++E){var C=r.codePointAt(E);if(C<=127){if(c>=v)break;a[c++]=C}else if(C<=2047){if(c+1>=v)break;a[c++]=192|C>>6,a[c++]=128|C&63}else if(C<=65535){if(c+2>=v)break;a[c++]=224|C>>12,a[c++]=128|C>>6&63,a[c++]=128|C&63}else{if(c+3>=v)break;C>1114111&&Vn("Invalid Unicode code point "+Mi(C)+" encountered when serializing a JS string to a UTF-8 string in wasm memory! (Valid unicode code points should be in range 0-0x10FFFF)."),a[c++]=240|C>>18,a[c++]=128|C>>12&63,a[c++]=128|C>>6&63,a[c++]=128|C&63,E++}}return a[c]=0,c-p},Et=(r,a,c)=>{var u=c>0?c:ct(r)+1,p=new Array(u),v=Ge(r,p,0,p.length);return a&&(p.length=v),p},jt=()=>{if(!lt.length){var r=null;if(o){var a=256,c=Buffer.alloc(a),u=0,p=process.stdin.fd;try{u=U.readSync(p,c,0,a)}catch(v){if(v.toString().includes("EOF"))u=0;else throw v}u>0&&(r=c.slice(0,u).toString("utf-8"))}else typeof window<"u"&&typeof window.prompt=="function"&&(r=window.prompt("Input: "),r!==null&&(r+=`
`));if(!r)return null;lt=Et(r,!0)}return lt.shift()},bt={ttys:[],init(){},shutdown(){},register(r,a){bt.ttys[r]={input:[],output:[],ops:a},M.registerDevice(r,bt.stream_ops)},stream_ops:{open(r){var a=bt.ttys[r.node.rdev];if(!a)throw new M.ErrnoError(43);r.tty=a,r.seekable=!1},close(r){r.tty.ops.fsync(r.tty)},fsync(r){r.tty.ops.fsync(r.tty)},read(r,a,c,u,p){if(!r.tty||!r.tty.ops.get_char)throw new M.ErrnoError(60);for(var v=0,E=0;E<u;E++){var C;try{C=r.tty.ops.get_char(r.tty)}catch{throw new M.ErrnoError(29)}if(C===void 0&&v===0)throw new M.ErrnoError(6);if(C==null)break;v++,a[c+E]=C}return v&&(r.node.atime=Date.now()),v},write(r,a,c,u,p){if(!r.tty||!r.tty.ops.put_char)throw new M.ErrnoError(60);try{for(var v=0;v<u;v++)r.tty.ops.put_char(r.tty,a[c+v])}catch{throw new M.ErrnoError(29)}return u&&(r.node.mtime=r.node.ctime=Date.now()),v}},default_tty_ops:{get_char(r){return jt()},put_char(r,a){a===null||a===10?(z(Sn(r.output)),r.output=[]):a!=0&&r.output.push(a)},fsync(r){r.output?.length>0&&(z(Sn(r.output)),r.output=[])},ioctl_tcgets(r){return{c_iflag:25856,c_oflag:5,c_cflag:191,c_lflag:35387,c_cc:[3,28,127,21,4,0,1,0,17,19,26,0,18,15,23,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}},ioctl_tcsets(r,a,c){return 0},ioctl_tiocgwinsz(r){return[24,80]}},default_tty1_ops:{put_char(r,a){a===null||a===10?(R(Sn(r.output)),r.output=[]):a!=0&&r.output.push(a)},fsync(r){r.output?.length>0&&(R(Sn(r.output)),r.output=[])}}},Pt=r=>{xe("internal error: mmapAlloc called but `emscripten_builtin_memalign` native symbol not exported")},qe={ops_table:null,mount(r){return qe.createNode(null,"/",16895,0)},createNode(r,a,c,u){if(M.isBlkdev(c)||M.isFIFO(c))throw new M.ErrnoError(63);qe.ops_table||={dir:{node:{getattr:qe.node_ops.getattr,setattr:qe.node_ops.setattr,lookup:qe.node_ops.lookup,mknod:qe.node_ops.mknod,rename:qe.node_ops.rename,unlink:qe.node_ops.unlink,rmdir:qe.node_ops.rmdir,readdir:qe.node_ops.readdir,symlink:qe.node_ops.symlink},stream:{llseek:qe.stream_ops.llseek}},file:{node:{getattr:qe.node_ops.getattr,setattr:qe.node_ops.setattr},stream:{llseek:qe.stream_ops.llseek,read:qe.stream_ops.read,write:qe.stream_ops.write,mmap:qe.stream_ops.mmap,msync:qe.stream_ops.msync}},link:{node:{getattr:qe.node_ops.getattr,setattr:qe.node_ops.setattr,readlink:qe.node_ops.readlink},stream:{}},chrdev:{node:{getattr:qe.node_ops.getattr,setattr:qe.node_ops.setattr},stream:M.chrdev_stream_ops}};var p=M.createNode(r,a,c,u);return M.isDir(p.mode)?(p.node_ops=qe.ops_table.dir.node,p.stream_ops=qe.ops_table.dir.stream,p.contents={}):M.isFile(p.mode)?(p.node_ops=qe.ops_table.file.node,p.stream_ops=qe.ops_table.file.stream,p.usedBytes=0,p.contents=null):M.isLink(p.mode)?(p.node_ops=qe.ops_table.link.node,p.stream_ops=qe.ops_table.link.stream):M.isChrdev(p.mode)&&(p.node_ops=qe.ops_table.chrdev.node,p.stream_ops=qe.ops_table.chrdev.stream),p.atime=p.mtime=p.ctime=Date.now(),r&&(r.contents[a]=p,r.atime=r.mtime=r.ctime=p.atime),p},getFileDataAsTypedArray(r){return r.contents?r.contents.subarray?r.contents.subarray(0,r.usedBytes):new Uint8Array(r.contents):new Uint8Array(0)},expandFileStorage(r,a){var c=r.contents?r.contents.length:0;if(!(c>=a)){var u=1024*1024;a=Math.max(a,c*(c<u?2:1.125)>>>0),c!=0&&(a=Math.max(a,256));var p=r.contents;r.contents=new Uint8Array(a),r.usedBytes>0&&r.contents.set(p.subarray(0,r.usedBytes),0)}},resizeFileStorage(r,a){if(r.usedBytes!=a)if(a==0)r.contents=null,r.usedBytes=0;else{var c=r.contents;r.contents=new Uint8Array(a),c&&r.contents.set(c.subarray(0,Math.min(a,r.usedBytes))),r.usedBytes=a}},node_ops:{getattr(r){var a={};return a.dev=M.isChrdev(r.mode)?r.id:1,a.ino=r.id,a.mode=r.mode,a.nlink=1,a.uid=0,a.gid=0,a.rdev=r.rdev,M.isDir(r.mode)?a.size=4096:M.isFile(r.mode)?a.size=r.usedBytes:M.isLink(r.mode)?a.size=r.link.length:a.size=0,a.atime=new Date(r.atime),a.mtime=new Date(r.mtime),a.ctime=new Date(r.ctime),a.blksize=4096,a.blocks=Math.ceil(a.size/a.blksize),a},setattr(r,a){for(let c of["mode","atime","mtime","ctime"])a[c]!=null&&(r[c]=a[c]);a.size!==void 0&&qe.resizeFileStorage(r,a.size)},lookup(r,a){throw new M.ErrnoError(44)},mknod(r,a,c,u){return qe.createNode(r,a,c,u)},rename(r,a,c){var u;try{u=M.lookupNode(a,c)}catch{}if(u){if(M.isDir(r.mode))for(var p in u.contents)throw new M.ErrnoError(55);M.hashRemoveNode(u)}delete r.parent.contents[r.name],a.contents[c]=r,r.name=c,a.ctime=a.mtime=r.parent.ctime=r.parent.mtime=Date.now()},unlink(r,a){delete r.contents[a],r.ctime=r.mtime=Date.now()},rmdir(r,a){var c=M.lookupNode(r,a);for(var u in c.contents)throw new M.ErrnoError(55);delete r.contents[a],r.ctime=r.mtime=Date.now()},readdir(r){return[".","..",...Object.keys(r.contents)]},symlink(r,a,c){var u=qe.createNode(r,a,41471,0);return u.link=c,u},readlink(r){if(!M.isLink(r.mode))throw new M.ErrnoError(28);return r.link}},stream_ops:{read(r,a,c,u,p){var v=r.node.contents;if(p>=r.node.usedBytes)return 0;var E=Math.min(r.node.usedBytes-p,u);if(k(E>=0),E>8&&v.subarray)a.set(v.subarray(p,p+E),c);else for(var C=0;C<E;C++)a[c+C]=v[p+C];return E},write(r,a,c,u,p,v){if(k(!(a instanceof ArrayBuffer)),a.buffer===rt.buffer&&(v=!1),!u)return 0;var E=r.node;if(E.mtime=E.ctime=Date.now(),a.subarray&&(!E.contents||E.contents.subarray)){if(v)return k(p===0,"canOwn must imply no weird position inside the file"),E.contents=a.subarray(c,c+u),E.usedBytes=u,u;if(E.usedBytes===0&&p===0)return E.contents=a.slice(c,c+u),E.usedBytes=u,u;if(p+u<=E.usedBytes)return E.contents.set(a.subarray(c,c+u),p),u}if(qe.expandFileStorage(E,p+u),E.contents.subarray&&a.subarray)E.contents.set(a.subarray(c,c+u),p);else for(var C=0;C<u;C++)E.contents[p+C]=a[c+C];return E.usedBytes=Math.max(E.usedBytes,p+u),u},llseek(r,a,c){var u=a;if(c===1?u+=r.position:c===2&&M.isFile(r.node.mode)&&(u+=r.node.usedBytes),u<0)throw new M.ErrnoError(28);return u},mmap(r,a,c,u,p){if(!M.isFile(r.node.mode))throw new M.ErrnoError(43);var v,E,C=r.node.contents;if(!(p&2)&&C&&C.buffer===rt.buffer)E=!1,v=C.byteOffset;else{if(E=!0,v=Pt(a),!v)throw new M.ErrnoError(48);C&&((c>0||c+a<C.length)&&(C.subarray?C=C.subarray(c,c+a):C=Array.prototype.slice.call(C,c,c+a)),rt.set(C,v))}return{ptr:v,allocated:E}},msync(r,a,c,u,p){return qe.stream_ops.write(r,a,0,u,c,!1),0}}},Oe=async r=>{var a=await T(r);return k(a,`Loading data file "${r}" failed (no arrayBuffer).`),new Uint8Array(a)},rn=(...r)=>M.createDataFile(...r),Mt=r=>{for(var a=r;;){if(!re[r])return r;r=a+Math.random()}},mn=[],Un=(r,a,c,u)=>{typeof Browser<"u"&&Browser.init();var p=!1;return mn.forEach(v=>{p||v.canHandle(a)&&(v.handle(r,a,c,u),p=!0)}),p},Gn=(r,a,c,u,p,v,E,C,N,$)=>{var ee=a?ze.resolve(be.join2(r,a)):r,ue=Mt(`cp ${ee}`);function pe(ce){function ve(Qe){$?.(),C||rn(r,a,Qe,u,p,N),v?.(),Xe(ue)}Un(ce,ee,ve,()=>{E?.(),Xe(ue)})||ve(ce)}Ce(ue),typeof c=="string"?Oe(c).then(pe,E):pe(c)},Ei=r=>{var a={r:0,"r+":2,w:577,"w+":578,a:1089,"a+":1090},c=a[r];if(typeof c>"u")throw new Error(`Unknown file open mode: ${r}`);return c},Rt=(r,a)=>{var c=0;return r&&(c|=365),a&&(c|=146),c},Wt=r=>An(Dh(r)),Hn={EPERM:63,ENOENT:44,ESRCH:71,EINTR:27,EIO:29,ENXIO:60,E2BIG:1,ENOEXEC:45,EBADF:8,ECHILD:12,EAGAIN:6,EWOULDBLOCK:6,ENOMEM:48,EACCES:2,EFAULT:21,ENOTBLK:105,EBUSY:10,EEXIST:20,EXDEV:75,ENODEV:43,ENOTDIR:54,EISDIR:31,EINVAL:28,ENFILE:41,EMFILE:33,ENOTTY:59,ETXTBSY:74,EFBIG:22,ENOSPC:51,ESPIPE:70,EROFS:69,EMLINK:34,EPIPE:64,EDOM:18,ERANGE:68,ENOMSG:49,EIDRM:24,ECHRNG:106,EL2NSYNC:156,EL3HLT:107,EL3RST:108,ELNRNG:109,EUNATCH:110,ENOCSI:111,EL2HLT:112,EDEADLK:16,ENOLCK:46,EBADE:113,EBADR:114,EXFULL:115,ENOANO:104,EBADRQC:103,EBADSLT:102,EDEADLOCK:16,EBFONT:101,ENOSTR:100,ENODATA:116,ETIME:117,ENOSR:118,ENONET:119,ENOPKG:120,EREMOTE:121,ENOLINK:47,EADV:122,ESRMNT:123,ECOMM:124,EPROTO:65,EMULTIHOP:36,EDOTDOT:125,EBADMSG:9,ENOTUNIQ:126,EBADFD:127,EREMCHG:128,ELIBACC:129,ELIBBAD:130,ELIBSCN:131,ELIBMAX:132,ELIBEXEC:133,ENOSYS:52,ENOTEMPTY:55,ENAMETOOLONG:37,ELOOP:32,EOPNOTSUPP:138,EPFNOSUPPORT:139,ECONNRESET:15,ENOBUFS:42,EAFNOSUPPORT:5,EPROTOTYPE:67,ENOTSOCK:57,ENOPROTOOPT:50,ESHUTDOWN:140,ECONNREFUSED:14,EADDRINUSE:3,ECONNABORTED:13,ENETUNREACH:40,ENETDOWN:38,ETIMEDOUT:73,EHOSTDOWN:142,EHOSTUNREACH:23,EINPROGRESS:26,EALREADY:7,EDESTADDRREQ:17,EMSGSIZE:35,EPROTONOSUPPORT:66,ESOCKTNOSUPPORT:137,EADDRNOTAVAIL:4,ENETRESET:39,EISCONN:30,ENOTCONN:53,ETOOMANYREFS:141,EUSERS:136,EDQUOT:19,ESTALE:72,ENOTSUP:138,ENOMEDIUM:148,EILSEQ:25,EOVERFLOW:61,ECANCELED:11,ENOTRECOVERABLE:56,EOWNERDEAD:62,ESTRPIPE:135},M={root:null,mounts:[],devices:{},streams:[],nextInode:1,nameTable:null,currentPath:"/",initialized:!1,ignorePermissions:!0,filesystems:null,syncFSRequests:0,readFiles:{},ErrnoError:class extends Error{name="ErrnoError";constructor(r){super(F?Wt(r):""),this.errno=r;for(var a in Hn)if(Hn[a]===r){this.code=a;break}}},FSStream:class{shared={};get object(){return this.node}set object(r){this.node=r}get isRead(){return(this.flags&2097155)!==1}get isWrite(){return(this.flags&2097155)!==0}get isAppend(){return this.flags&1024}get flags(){return this.shared.flags}set flags(r){this.shared.flags=r}get position(){return this.shared.position}set position(r){this.shared.position=r}},FSNode:class{node_ops={};stream_ops={};readMode=365;writeMode=146;mounted=null;constructor(r,a,c,u){r||(r=this),this.parent=r,this.mount=r.mount,this.id=M.nextInode++,this.name=a,this.mode=c,this.rdev=u,this.atime=this.mtime=this.ctime=Date.now()}get read(){return(this.mode&this.readMode)===this.readMode}set read(r){r?this.mode|=this.readMode:this.mode&=~this.readMode}get write(){return(this.mode&this.writeMode)===this.writeMode}set write(r){r?this.mode|=this.writeMode:this.mode&=~this.writeMode}get isFolder(){return M.isDir(this.mode)}get isDevice(){return M.isChrdev(this.mode)}},lookupPath(r,a={}){if(!r)throw new M.ErrnoError(44);a.follow_mount??=!0,be.isAbs(r)||(r=M.cwd()+"/"+r);e:for(var c=0;c<40;c++){for(var u=r.split("/").filter($=>!!$),p=M.root,v="/",E=0;E<u.length;E++){var C=E===u.length-1;if(C&&a.parent)break;if(u[E]!=="."){if(u[E]===".."){if(v=be.dirname(v),M.isRoot(p)){r=v+"/"+u.slice(E+1).join("/");continue e}else p=p.parent;continue}v=be.join2(v,u[E]);try{p=M.lookupNode(p,u[E])}catch($){if($?.errno===44&&C&&a.noent_okay)return{path:v};throw $}if(M.isMountpoint(p)&&(!C||a.follow_mount)&&(p=p.mounted.root),M.isLink(p.mode)&&(!C||a.follow)){if(!p.node_ops.readlink)throw new M.ErrnoError(52);var N=p.node_ops.readlink(p);be.isAbs(N)||(N=be.dirname(v)+"/"+N),r=N+"/"+u.slice(E+1).join("/");continue e}}}return{path:v,node:p}}throw new M.ErrnoError(32)},getPath(r){for(var a;;){if(M.isRoot(r)){var c=r.mount.mountpoint;return a?c[c.length-1]!=="/"?`${c}/${a}`:c+a:c}a=a?`${r.name}/${a}`:r.name,r=r.parent}},hashName(r,a){for(var c=0,u=0;u<a.length;u++)c=(c<<5)-c+a.charCodeAt(u)|0;return(r+c>>>0)%M.nameTable.length},hashAddNode(r){var a=M.hashName(r.parent.id,r.name);r.name_next=M.nameTable[a],M.nameTable[a]=r},hashRemoveNode(r){var a=M.hashName(r.parent.id,r.name);if(M.nameTable[a]===r)M.nameTable[a]=r.name_next;else for(var c=M.nameTable[a];c;){if(c.name_next===r){c.name_next=r.name_next;break}c=c.name_next}},lookupNode(r,a){var c=M.mayLookup(r);if(c)throw new M.ErrnoError(c);for(var u=M.hashName(r.id,a),p=M.nameTable[u];p;p=p.name_next){var v=p.name;if(p.parent.id===r.id&&v===a)return p}return M.lookup(r,a)},createNode(r,a,c,u){k(typeof r=="object");var p=new M.FSNode(r,a,c,u);return M.hashAddNode(p),p},destroyNode(r){M.hashRemoveNode(r)},isRoot(r){return r===r.parent},isMountpoint(r){return!!r.mounted},isFile(r){return(r&61440)===32768},isDir(r){return(r&61440)===16384},isLink(r){return(r&61440)===40960},isChrdev(r){return(r&61440)===8192},isBlkdev(r){return(r&61440)===24576},isFIFO(r){return(r&61440)===4096},isSocket(r){return(r&49152)===49152},flagsToPermissionString(r){var a=["r","w","rw"][r&3];return r&512&&(a+="w"),a},nodePermissions(r,a){return M.ignorePermissions?0:a.includes("r")&&!(r.mode&292)||a.includes("w")&&!(r.mode&146)||a.includes("x")&&!(r.mode&73)?2:0},mayLookup(r){if(!M.isDir(r.mode))return 54;var a=M.nodePermissions(r,"x");return a||(r.node_ops.lookup?0:2)},mayCreate(r,a){if(!M.isDir(r.mode))return 54;try{var c=M.lookupNode(r,a);return 20}catch{}return M.nodePermissions(r,"wx")},mayDelete(r,a,c){var u;try{u=M.lookupNode(r,a)}catch(v){return v.errno}var p=M.nodePermissions(r,"wx");if(p)return p;if(c){if(!M.isDir(u.mode))return 54;if(M.isRoot(u)||M.getPath(u)===M.cwd())return 10}else if(M.isDir(u.mode))return 31;return 0},mayOpen(r,a){return r?M.isLink(r.mode)?32:M.isDir(r.mode)&&(M.flagsToPermissionString(a)!=="r"||a&576)?31:M.nodePermissions(r,M.flagsToPermissionString(a)):44},checkOpExists(r,a){if(!r)throw new M.ErrnoError(a);return r},MAX_OPEN_FDS:4096,nextfd(){for(var r=0;r<=M.MAX_OPEN_FDS;r++)if(!M.streams[r])return r;throw new M.ErrnoError(33)},getStreamChecked(r){var a=M.getStream(r);if(!a)throw new M.ErrnoError(8);return a},getStream:r=>M.streams[r],createStream(r,a=-1){return k(a>=-1),r=Object.assign(new M.FSStream,r),a==-1&&(a=M.nextfd()),r.fd=a,M.streams[a]=r,r},closeStream(r){M.streams[r]=null},dupStream(r,a=-1){var c=M.createStream(r,a);return c.stream_ops?.dup?.(c),c},doSetAttr(r,a,c){var u=r?.stream_ops.setattr,p=u?r:a;u??=a.node_ops.setattr,M.checkOpExists(u,63),u(p,c)},chrdev_stream_ops:{open(r){var a=M.getDevice(r.node.rdev);r.stream_ops=a.stream_ops,r.stream_ops.open?.(r)},llseek(){throw new M.ErrnoError(70)}},major:r=>r>>8,minor:r=>r&255,makedev:(r,a)=>r<<8|a,registerDevice(r,a){M.devices[r]={stream_ops:a}},getDevice:r=>M.devices[r],getMounts(r){for(var a=[],c=[r];c.length;){var u=c.pop();a.push(u),c.push(...u.mounts)}return a},syncfs(r,a){typeof r=="function"&&(a=r,r=!1),M.syncFSRequests++,M.syncFSRequests>1&&R(`warning: ${M.syncFSRequests} FS.syncfs operations in flight at once, probably just doing extra work`);var c=M.getMounts(M.root.mount),u=0;function p(E){return k(M.syncFSRequests>0),M.syncFSRequests--,a(E)}function v(E){if(E)return v.errored?void 0:(v.errored=!0,p(E));++u>=c.length&&p(null)}c.forEach(E=>{if(!E.type.syncfs)return v(null);E.type.syncfs(E,r,v)})},mount(r,a,c){if(typeof r=="string")throw r;var u=c==="/",p=!c,v;if(u&&M.root)throw new M.ErrnoError(10);if(!u&&!p){var E=M.lookupPath(c,{follow_mount:!1});if(c=E.path,v=E.node,M.isMountpoint(v))throw new M.ErrnoError(10);if(!M.isDir(v.mode))throw new M.ErrnoError(54)}var C={type:r,opts:a,mountpoint:c,mounts:[]},N=r.mount(C);return N.mount=C,C.root=N,u?M.root=N:v&&(v.mounted=C,v.mount&&v.mount.mounts.push(C)),N},unmount(r){var a=M.lookupPath(r,{follow_mount:!1});if(!M.isMountpoint(a.node))throw new M.ErrnoError(28);var c=a.node,u=c.mounted,p=M.getMounts(u);Object.keys(M.nameTable).forEach(E=>{for(var C=M.nameTable[E];C;){var N=C.name_next;p.includes(C.mount)&&M.destroyNode(C),C=N}}),c.mounted=null;var v=c.mount.mounts.indexOf(u);k(v!==-1),c.mount.mounts.splice(v,1)},lookup(r,a){return r.node_ops.lookup(r,a)},mknod(r,a,c){var u=M.lookupPath(r,{parent:!0}),p=u.node,v=be.basename(r);if(!v)throw new M.ErrnoError(28);if(v==="."||v==="..")throw new M.ErrnoError(20);var E=M.mayCreate(p,v);if(E)throw new M.ErrnoError(E);if(!p.node_ops.mknod)throw new M.ErrnoError(63);return p.node_ops.mknod(p,v,a,c)},statfs(r){return M.statfsNode(M.lookupPath(r,{follow:!0}).node)},statfsStream(r){return M.statfsNode(r.node)},statfsNode(r){var a={bsize:4096,frsize:4096,blocks:1e6,bfree:5e5,bavail:5e5,files:M.nextInode,ffree:M.nextInode-1,fsid:42,flags:2,namelen:255};return r.node_ops.statfs&&Object.assign(a,r.node_ops.statfs(r.mount.opts.root)),a},create(r,a=438){return a&=4095,a|=32768,M.mknod(r,a,0)},mkdir(r,a=511){return a&=1023,a|=16384,M.mknod(r,a,0)},mkdirTree(r,a){var c=r.split("/"),u="";for(var p of c)if(p){(u||be.isAbs(r))&&(u+="/"),u+=p;try{M.mkdir(u,a)}catch(v){if(v.errno!=20)throw v}}},mkdev(r,a,c){return typeof c>"u"&&(c=a,a=438),a|=8192,M.mknod(r,a,c)},symlink(r,a){if(!ze.resolve(r))throw new M.ErrnoError(44);var c=M.lookupPath(a,{parent:!0}),u=c.node;if(!u)throw new M.ErrnoError(44);var p=be.basename(a),v=M.mayCreate(u,p);if(v)throw new M.ErrnoError(v);if(!u.node_ops.symlink)throw new M.ErrnoError(63);return u.node_ops.symlink(u,p,r)},rename(r,a){var c=be.dirname(r),u=be.dirname(a),p=be.basename(r),v=be.basename(a),E,C,N;if(E=M.lookupPath(r,{parent:!0}),C=E.node,E=M.lookupPath(a,{parent:!0}),N=E.node,!C||!N)throw new M.ErrnoError(44);if(C.mount!==N.mount)throw new M.ErrnoError(75);var $=M.lookupNode(C,p),ee=ze.relative(r,u);if(ee.charAt(0)!==".")throw new M.ErrnoError(28);if(ee=ze.relative(a,c),ee.charAt(0)!==".")throw new M.ErrnoError(55);var ue;try{ue=M.lookupNode(N,v)}catch{}if($!==ue){var pe=M.isDir($.mode),ce=M.mayDelete(C,p,pe);if(ce)throw new M.ErrnoError(ce);if(ce=ue?M.mayDelete(N,v,pe):M.mayCreate(N,v),ce)throw new M.ErrnoError(ce);if(!C.node_ops.rename)throw new M.ErrnoError(63);if(M.isMountpoint($)||ue&&M.isMountpoint(ue))throw new M.ErrnoError(10);if(N!==C&&(ce=M.nodePermissions(C,"w"),ce))throw new M.ErrnoError(ce);M.hashRemoveNode($);try{C.node_ops.rename($,N,v),$.parent=N}catch(ve){throw ve}finally{M.hashAddNode($)}}},rmdir(r){var a=M.lookupPath(r,{parent:!0}),c=a.node,u=be.basename(r),p=M.lookupNode(c,u),v=M.mayDelete(c,u,!0);if(v)throw new M.ErrnoError(v);if(!c.node_ops.rmdir)throw new M.ErrnoError(63);if(M.isMountpoint(p))throw new M.ErrnoError(10);c.node_ops.rmdir(c,u),M.destroyNode(p)},readdir(r){var a=M.lookupPath(r,{follow:!0}),c=a.node,u=M.checkOpExists(c.node_ops.readdir,54);return u(c)},unlink(r){var a=M.lookupPath(r,{parent:!0}),c=a.node;if(!c)throw new M.ErrnoError(44);var u=be.basename(r),p=M.lookupNode(c,u),v=M.mayDelete(c,u,!1);if(v)throw new M.ErrnoError(v);if(!c.node_ops.unlink)throw new M.ErrnoError(63);if(M.isMountpoint(p))throw new M.ErrnoError(10);c.node_ops.unlink(c,u),M.destroyNode(p)},readlink(r){var a=M.lookupPath(r),c=a.node;if(!c)throw new M.ErrnoError(44);if(!c.node_ops.readlink)throw new M.ErrnoError(28);return c.node_ops.readlink(c)},stat(r,a){var c=M.lookupPath(r,{follow:!a}),u=c.node,p=M.checkOpExists(u.node_ops.getattr,63);return p(u)},fstat(r){var a=M.getStreamChecked(r),c=a.node,u=a.stream_ops.getattr,p=u?a:c;return u??=c.node_ops.getattr,M.checkOpExists(u,63),u(p)},lstat(r){return M.stat(r,!0)},doChmod(r,a,c,u){M.doSetAttr(r,a,{mode:c&4095|a.mode&-4096,ctime:Date.now(),dontFollow:u})},chmod(r,a,c){var u;if(typeof r=="string"){var p=M.lookupPath(r,{follow:!c});u=p.node}else u=r;M.doChmod(null,u,a,c)},lchmod(r,a){M.chmod(r,a,!0)},fchmod(r,a){var c=M.getStreamChecked(r);M.doChmod(c,c.node,a,!1)},doChown(r,a,c){M.doSetAttr(r,a,{timestamp:Date.now(),dontFollow:c})},chown(r,a,c,u){var p;if(typeof r=="string"){var v=M.lookupPath(r,{follow:!u});p=v.node}else p=r;M.doChown(null,p,u)},lchown(r,a,c){M.chown(r,a,c,!0)},fchown(r,a,c){var u=M.getStreamChecked(r);M.doChown(u,u.node,!1)},doTruncate(r,a,c){if(M.isDir(a.mode))throw new M.ErrnoError(31);if(!M.isFile(a.mode))throw new M.ErrnoError(28);var u=M.nodePermissions(a,"w");if(u)throw new M.ErrnoError(u);M.doSetAttr(r,a,{size:c,timestamp:Date.now()})},truncate(r,a){if(a<0)throw new M.ErrnoError(28);var c;if(typeof r=="string"){var u=M.lookupPath(r,{follow:!0});c=u.node}else c=r;M.doTruncate(null,c,a)},ftruncate(r,a){var c=M.getStreamChecked(r);if(a<0||(c.flags&2097155)===0)throw new M.ErrnoError(28);M.doTruncate(c,c.node,a)},utime(r,a,c){var u=M.lookupPath(r,{follow:!0}),p=u.node,v=M.checkOpExists(p.node_ops.setattr,63);v(p,{atime:a,mtime:c})},open(r,a,c=438){if(r==="")throw new M.ErrnoError(44);a=typeof a=="string"?Ei(a):a,a&64?c=c&4095|32768:c=0;var u,p;if(typeof r=="object")u=r;else{p=r.endsWith("/");var v=M.lookupPath(r,{follow:!(a&131072),noent_okay:!0});u=v.node,r=v.path}var E=!1;if(a&64)if(u){if(a&128)throw new M.ErrnoError(20)}else{if(p)throw new M.ErrnoError(31);u=M.mknod(r,c|511,0),E=!0}if(!u)throw new M.ErrnoError(44);if(M.isChrdev(u.mode)&&(a&=-513),a&65536&&!M.isDir(u.mode))throw new M.ErrnoError(54);if(!E){var C=M.mayOpen(u,a);if(C)throw new M.ErrnoError(C)}a&512&&!E&&M.truncate(u,0),a&=-131713;var N=M.createStream({node:u,path:M.getPath(u),flags:a,seekable:!0,position:0,stream_ops:u.stream_ops,ungotten:[],error:!1});return N.stream_ops.open&&N.stream_ops.open(N),E&&M.chmod(u,c&511),t.logReadFiles&&!(a&1)&&(r in M.readFiles||(M.readFiles[r]=1)),N},close(r){if(M.isClosed(r))throw new M.ErrnoError(8);r.getdents&&(r.getdents=null);try{r.stream_ops.close&&r.stream_ops.close(r)}catch(a){throw a}finally{M.closeStream(r.fd)}r.fd=null},isClosed(r){return r.fd===null},llseek(r,a,c){if(M.isClosed(r))throw new M.ErrnoError(8);if(!r.seekable||!r.stream_ops.llseek)throw new M.ErrnoError(70);if(c!=0&&c!=1&&c!=2)throw new M.ErrnoError(28);return r.position=r.stream_ops.llseek(r,a,c),r.ungotten=[],r.position},read(r,a,c,u,p){if(k(c>=0),u<0||p<0)throw new M.ErrnoError(28);if(M.isClosed(r))throw new M.ErrnoError(8);if((r.flags&2097155)===1)throw new M.ErrnoError(8);if(M.isDir(r.node.mode))throw new M.ErrnoError(31);if(!r.stream_ops.read)throw new M.ErrnoError(28);var v=typeof p<"u";if(!v)p=r.position;else if(!r.seekable)throw new M.ErrnoError(70);var E=r.stream_ops.read(r,a,c,u,p);return v||(r.position+=E),E},write(r,a,c,u,p,v){if(k(c>=0),u<0||p<0)throw new M.ErrnoError(28);if(M.isClosed(r))throw new M.ErrnoError(8);if((r.flags&2097155)===0)throw new M.ErrnoError(8);if(M.isDir(r.node.mode))throw new M.ErrnoError(31);if(!r.stream_ops.write)throw new M.ErrnoError(28);r.seekable&&r.flags&1024&&M.llseek(r,0,2);var E=typeof p<"u";if(!E)p=r.position;else if(!r.seekable)throw new M.ErrnoError(70);var C=r.stream_ops.write(r,a,c,u,p,v);return E||(r.position+=C),C},mmap(r,a,c,u,p){if((u&2)!==0&&(p&2)===0&&(r.flags&2097155)!==2)throw new M.ErrnoError(2);if((r.flags&2097155)===1)throw new M.ErrnoError(2);if(!r.stream_ops.mmap)throw new M.ErrnoError(43);if(!a)throw new M.ErrnoError(28);return r.stream_ops.mmap(r,a,c,u,p)},msync(r,a,c,u,p){return k(c>=0),r.stream_ops.msync?r.stream_ops.msync(r,a,c,u,p):0},ioctl(r,a,c){if(!r.stream_ops.ioctl)throw new M.ErrnoError(59);return r.stream_ops.ioctl(r,a,c)},readFile(r,a={}){if(a.flags=a.flags||0,a.encoding=a.encoding||"binary",a.encoding!=="utf8"&&a.encoding!=="binary")throw new Error(`Invalid encoding type "${a.encoding}"`);var c=M.open(r,a.flags),u=M.stat(r),p=u.size,v=new Uint8Array(p);return M.read(c,v,0,p,0),a.encoding==="utf8"&&(v=Sn(v)),M.close(c),v},writeFile(r,a,c={}){c.flags=c.flags||577;var u=M.open(r,c.flags,c.mode);if(typeof a=="string"&&(a=new Uint8Array(Et(a,!0))),ArrayBuffer.isView(a))M.write(u,a,0,a.byteLength,void 0,c.canOwn);else throw new Error("Unsupported data type");M.close(u)},cwd:()=>M.currentPath,chdir(r){var a=M.lookupPath(r,{follow:!0});if(a.node===null)throw new M.ErrnoError(44);if(!M.isDir(a.node.mode))throw new M.ErrnoError(54);var c=M.nodePermissions(a.node,"x");if(c)throw new M.ErrnoError(c);M.currentPath=a.path},createDefaultDirectories(){M.mkdir("/tmp"),M.mkdir("/home"),M.mkdir("/home/web_user")},createDefaultDevices(){M.mkdir("/dev"),M.registerDevice(M.makedev(1,3),{read:()=>0,write:(u,p,v,E,C)=>E,llseek:()=>0}),M.mkdev("/dev/null",M.makedev(1,3)),bt.register(M.makedev(5,0),bt.default_tty_ops),bt.register(M.makedev(6,0),bt.default_tty1_ops),M.mkdev("/dev/tty",M.makedev(5,0)),M.mkdev("/dev/tty1",M.makedev(6,0));var r=new Uint8Array(1024),a=0,c=()=>(a===0&&(Ve(r),a=r.byteLength),r[--a]);M.createDevice("/dev","random",c),M.createDevice("/dev","urandom",c),M.mkdir("/dev/shm"),M.mkdir("/dev/shm/tmp")},createSpecialDirectories(){M.mkdir("/proc");var r=M.mkdir("/proc/self");M.mkdir("/proc/self/fd"),M.mount({mount(){var a=M.createNode(r,"fd",16895,73);return a.stream_ops={llseek:qe.stream_ops.llseek},a.node_ops={lookup(c,u){var p=+u,v=M.getStreamChecked(p),E={parent:null,mount:{mountpoint:"fake"},node_ops:{readlink:()=>v.path},id:p+1};return E.parent=E,E},readdir(){return Array.from(M.streams.entries()).filter(([c,u])=>u).map(([c,u])=>c.toString())}},a}},{},"/proc/self/fd")},createStandardStreams(r,a,c){r?M.createDevice("/dev","stdin",r):M.symlink("/dev/tty","/dev/stdin"),a?M.createDevice("/dev","stdout",null,a):M.symlink("/dev/tty","/dev/stdout"),c?M.createDevice("/dev","stderr",null,c):M.symlink("/dev/tty1","/dev/stderr");var u=M.open("/dev/stdin",0),p=M.open("/dev/stdout",1),v=M.open("/dev/stderr",1);k(u.fd===0,`invalid handle for stdin (${u.fd})`),k(p.fd===1,`invalid handle for stdout (${p.fd})`),k(v.fd===2,`invalid handle for stderr (${v.fd})`)},staticInit(){M.nameTable=new Array(4096),M.mount(qe,{},"/"),M.createDefaultDirectories(),M.createDefaultDevices(),M.createSpecialDirectories(),M.filesystems={MEMFS:qe}},init(r,a,c){k(!M.initialized,"FS.init was previously called. If you want to initialize later with custom parameters, remove any earlier calls (note that one is automatically added to the generated code)"),M.initialized=!0,r??=t.stdin,a??=t.stdout,c??=t.stderr,M.createStandardStreams(r,a,c)},quit(){M.initialized=!1,Rl(0);for(var r of M.streams)r&&M.close(r)},findObject(r,a){var c=M.analyzePath(r,a);return c.exists?c.object:null},analyzePath(r,a){try{var c=M.lookupPath(r,{follow:!a});r=c.path}catch{}var u={isRoot:!1,exists:!1,error:0,name:null,path:null,object:null,parentExists:!1,parentPath:null,parentObject:null};try{var c=M.lookupPath(r,{parent:!0});u.parentExists=!0,u.parentPath=c.path,u.parentObject=c.node,u.name=be.basename(r),c=M.lookupPath(r,{follow:!a}),u.exists=!0,u.path=c.path,u.object=c.node,u.name=c.node.name,u.isRoot=c.path==="/"}catch(p){u.error=p.errno}return u},createPath(r,a,c,u){r=typeof r=="string"?r:M.getPath(r);for(var p=a.split("/").reverse();p.length;){var v=p.pop();if(v){var E=be.join2(r,v);try{M.mkdir(E)}catch(C){if(C.errno!=20)throw C}r=E}}return E},createFile(r,a,c,u,p){var v=be.join2(typeof r=="string"?r:M.getPath(r),a),E=Rt(u,p);return M.create(v,E)},createDataFile(r,a,c,u,p,v){var E=a;r&&(r=typeof r=="string"?r:M.getPath(r),E=a?be.join2(r,a):r);var C=Rt(u,p),N=M.create(E,C);if(c){if(typeof c=="string"){for(var $=new Array(c.length),ee=0,ue=c.length;ee<ue;++ee)$[ee]=c.charCodeAt(ee);c=$}M.chmod(N,C|146);var pe=M.open(N,577);M.write(pe,c,0,c.length,0,v),M.close(pe),M.chmod(N,C)}},createDevice(r,a,c,u){var p=be.join2(typeof r=="string"?r:M.getPath(r),a),v=Rt(!!c,!!u);M.createDevice.major??=64;var E=M.makedev(M.createDevice.major++,0);return M.registerDevice(E,{open(C){C.seekable=!1},close(C){u?.buffer?.length&&u(10)},read(C,N,$,ee,ue){for(var pe=0,ce=0;ce<ee;ce++){var ve;try{ve=c()}catch{throw new M.ErrnoError(29)}if(ve===void 0&&pe===0)throw new M.ErrnoError(6);if(ve==null)break;pe++,N[$+ce]=ve}return pe&&(C.node.atime=Date.now()),pe},write(C,N,$,ee,ue){for(var pe=0;pe<ee;pe++)try{u(N[$+pe])}catch{throw new M.ErrnoError(29)}return ee&&(C.node.mtime=C.node.ctime=Date.now()),pe}}),M.mkdev(p,v,E)},forceLoadFile(r){if(r.isDevice||r.isFolder||r.link||r.contents)return!0;if(typeof XMLHttpRequest<"u")throw new Error("Lazy loading should have been performed (contents set) in createLazyFile, but it was not. Lazy loading only works in web workers. Use --embed-file or --preload-file in emcc on the main thread.");try{r.contents=P(r.url),r.usedBytes=r.contents.length}catch{throw new M.ErrnoError(29)}},createLazyFile(r,a,c,u,p){class v{lengthKnown=!1;chunks=[];get(ce){if(!(ce>this.length-1||ce<0)){var ve=ce%this.chunkSize,Qe=ce/this.chunkSize|0;return this.getter(Qe)[ve]}}setDataGetter(ce){this.getter=ce}cacheLength(){var ce=new XMLHttpRequest;if(ce.open("HEAD",c,!1),ce.send(null),!(ce.status>=200&&ce.status<300||ce.status===304))throw new Error("Couldn't load "+c+". Status: "+ce.status);var ve=Number(ce.getResponseHeader("Content-length")),Qe,yt=(Qe=ce.getResponseHeader("Accept-Ranges"))&&Qe==="bytes",ft=(Qe=ce.getResponseHeader("Content-Encoding"))&&Qe==="gzip",kt=1024*1024;yt||(kt=ve);var At=(Kt,gn)=>{if(Kt>gn)throw new Error("invalid range ("+Kt+", "+gn+") or no bytes requested!");if(gn>ve-1)throw new Error("only "+ve+" bytes available! programmer error!");var Nt=new XMLHttpRequest;if(Nt.open("GET",c,!1),ve!==kt&&Nt.setRequestHeader("Range","bytes="+Kt+"-"+gn),Nt.responseType="arraybuffer",Nt.overrideMimeType&&Nt.overrideMimeType("text/plain; charset=x-user-defined"),Nt.send(null),!(Nt.status>=200&&Nt.status<300||Nt.status===304))throw new Error("Couldn't load "+c+". Status: "+Nt.status);return Nt.response!==void 0?new Uint8Array(Nt.response||[]):Et(Nt.responseText||"",!0)},cn=this;cn.setDataGetter(Kt=>{var gn=Kt*kt,Nt=(Kt+1)*kt-1;if(Nt=Math.min(Nt,ve-1),typeof cn.chunks[Kt]>"u"&&(cn.chunks[Kt]=At(gn,Nt)),typeof cn.chunks[Kt]>"u")throw new Error("doXHR failed!");return cn.chunks[Kt]}),(ft||!ve)&&(kt=ve=1,ve=this.getter(0).length,kt=ve,z("LazyFiles on gzip forces download of the whole file when length is accessed")),this._length=ve,this._chunkSize=kt,this.lengthKnown=!0}get length(){return this.lengthKnown||this.cacheLength(),this._length}get chunkSize(){return this.lengthKnown||this.cacheLength(),this._chunkSize}}if(typeof XMLHttpRequest<"u"){if(!s)throw"Cannot do synchronous binary XHRs outside webworkers in modern browsers. Use --embed-file or --preload-file in emcc";var E=new v,C={isDevice:!1,contents:E}}else var C={isDevice:!1,url:c};var N=M.createFile(r,a,C,u,p);C.contents?N.contents=C.contents:C.url&&(N.contents=null,N.url=C.url),Object.defineProperties(N,{usedBytes:{get:function(){return this.contents.length}}});var $={},ee=Object.keys(N.stream_ops);ee.forEach(pe=>{var ce=N.stream_ops[pe];$[pe]=(...ve)=>(M.forceLoadFile(N),ce(...ve))});function ue(pe,ce,ve,Qe,yt){var ft=pe.node.contents;if(yt>=ft.length)return 0;var kt=Math.min(ft.length-yt,Qe);if(k(kt>=0),ft.slice)for(var At=0;At<kt;At++)ce[ve+At]=ft[yt+At];else for(var At=0;At<kt;At++)ce[ve+At]=ft.get(yt+At);return kt}return $.read=(pe,ce,ve,Qe,yt)=>(M.forceLoadFile(N),ue(pe,ce,ve,Qe,yt)),$.mmap=(pe,ce,ve,Qe,yt)=>{M.forceLoadFile(N);var ft=Pt(ce);if(!ft)throw new M.ErrnoError(48);return ue(pe,rt,ft,ce,ve),{ptr:ft,allocated:!0}},N.stream_ops=$,N},absolutePath(){xe("FS.absolutePath has been removed; use PATH_FS.resolve instead")},createFolder(){xe("FS.createFolder has been removed; use FS.mkdir instead")},createLink(){xe("FS.createLink has been removed; use FS.symlink instead")},joinPath(){xe("FS.joinPath has been removed; use PATH.join instead")},mmapAlloc(){xe("FS.mmapAlloc has been replaced by the top level function mmapAlloc")},standardizePath(){xe("FS.standardizePath has been removed; use PATH.normalize instead")}},Tt={DEFAULT_POLLMASK:5,calculateAt(r,a,c){if(be.isAbs(a))return a;var u;if(r===-100)u=M.cwd();else{var p=Tt.getStreamFromFD(r);u=p.path}if(a.length==0){if(!c)throw new M.ErrnoError(44);return u}return u+"/"+a},writeStat(r,a){Ie[r>>2]=a.dev,Ie[r+4>>2]=a.mode,Ue[r+8>>2]=a.nlink,Ie[r+12>>2]=a.uid,Ie[r+16>>2]=a.gid,Ie[r+20>>2]=a.rdev,Dt[r+24>>3]=BigInt(a.size),Ie[r+32>>2]=4096,Ie[r+36>>2]=a.blocks;var c=a.atime.getTime(),u=a.mtime.getTime(),p=a.ctime.getTime();return Dt[r+40>>3]=BigInt(Math.floor(c/1e3)),Ue[r+48>>2]=c%1e3*1e3*1e3,Dt[r+56>>3]=BigInt(Math.floor(u/1e3)),Ue[r+64>>2]=u%1e3*1e3*1e3,Dt[r+72>>3]=BigInt(Math.floor(p/1e3)),Ue[r+80>>2]=p%1e3*1e3*1e3,Dt[r+88>>3]=BigInt(a.ino),0},writeStatFs(r,a){Ie[r+4>>2]=a.bsize,Ie[r+40>>2]=a.bsize,Ie[r+8>>2]=a.blocks,Ie[r+12>>2]=a.bfree,Ie[r+16>>2]=a.bavail,Ie[r+20>>2]=a.files,Ie[r+24>>2]=a.ffree,Ie[r+28>>2]=a.fsid,Ie[r+44>>2]=a.flags,Ie[r+36>>2]=a.namelen},doMsync(r,a,c,u,p){if(!M.isFile(a.node.mode))throw new M.ErrnoError(43);if(u&2)return 0;var v=tt.slice(r,r+c);M.msync(a,v,p,c,u)},getStreamFromFD(r){var a=M.getStreamChecked(r);return a},varargs:void 0,getStr(r){var a=An(r);return a}};function wi(r,a,c){try{var u=Tt.getStreamFromFD(r);if(k(!c),u.fd===a)return-28;if(a<0||a>=M.MAX_OPEN_FDS)return-8;var p=M.getStream(a);return p&&M.close(p),M.dupStream(u,a).fd}catch(v){if(typeof M>"u"||v.name!=="ErrnoError")throw v;return-v.errno}}var Wi=()=>{k(Tt.varargs!=null);var r=Ie[+Tt.varargs>>2];return Tt.varargs+=4,r},fr=Wi;function Vd(r,a,c){Tt.varargs=c;try{var u=Tt.getStreamFromFD(r);switch(a){case 0:{var p=Wi();if(p<0)return-28;for(;M.streams[p];)p++;var v;return v=M.dupStream(u,p),v.fd}case 1:case 2:return 0;case 3:return u.flags;case 4:{var p=Wi();return u.flags|=p,0}case 12:{var p=fr(),E=0;return St[p+E>>1]=2,0}case 13:case 14:return 0}return-28}catch(C){if(typeof M>"u"||C.name!=="ErrnoError")throw C;return-C.errno}}function Gd(r,a){try{return Tt.writeStat(a,M.fstat(r))}catch(c){if(typeof M>"u"||c.name!=="ErrnoError")throw c;return-c.errno}}function Hd(r,a,c){Tt.varargs=c;try{var u=Tt.getStreamFromFD(r);switch(a){case 21509:return u.tty?0:-59;case 21505:{if(!u.tty)return-59;if(u.tty.ops.ioctl_tcgets){var p=u.tty.ops.ioctl_tcgets(u),v=fr();Ie[v>>2]=p.c_iflag||0,Ie[v+4>>2]=p.c_oflag||0,Ie[v+8>>2]=p.c_cflag||0,Ie[v+12>>2]=p.c_lflag||0;for(var E=0;E<32;E++)rt[v+E+17]=p.c_cc[E]||0;return 0}return 0}case 21510:case 21511:case 21512:return u.tty?0:-59;case 21506:case 21507:case 21508:{if(!u.tty)return-59;if(u.tty.ops.ioctl_tcsets){for(var v=fr(),C=Ie[v>>2],N=Ie[v+4>>2],$=Ie[v+8>>2],ee=Ie[v+12>>2],ue=[],E=0;E<32;E++)ue.push(rt[v+E+17]);return u.tty.ops.ioctl_tcsets(u.tty,a,{c_iflag:C,c_oflag:N,c_cflag:$,c_lflag:ee,c_cc:ue})}return 0}case 21519:{if(!u.tty)return-59;var v=fr();return Ie[v>>2]=0,0}case 21520:return u.tty?-28:-59;case 21531:{var v=fr();return M.ioctl(u,a,v)}case 21523:{if(!u.tty)return-59;if(u.tty.ops.ioctl_tiocgwinsz){var pe=u.tty.ops.ioctl_tiocgwinsz(u.tty),v=fr();St[v>>1]=pe[0],St[v+2>>1]=pe[1]}return 0}case 21524:return u.tty?0:-59;case 21515:return u.tty?0:-59;default:return-28}}catch(ce){if(typeof M>"u"||ce.name!=="ErrnoError")throw ce;return-ce.errno}}function Wd(r,a){try{return r=Tt.getStr(r),Tt.writeStat(a,M.lstat(r))}catch(c){if(typeof M>"u"||c.name!=="ErrnoError")throw c;return-c.errno}}function Xd(r,a,c,u){try{a=Tt.getStr(a);var p=u&256,v=u&4096;return u=u&-6401,k(!u,`unknown flags in __syscall_newfstatat: ${u}`),a=Tt.calculateAt(r,a,v),Tt.writeStat(c,p?M.lstat(a):M.stat(a))}catch(E){if(typeof M>"u"||E.name!=="ErrnoError")throw E;return-E.errno}}function $d(r,a,c,u){Tt.varargs=u;try{a=Tt.getStr(a),a=Tt.calculateAt(r,a);var p=u?Wi():0;return M.open(a,c,p).fd}catch(v){if(typeof M>"u"||v.name!=="ErrnoError")throw v;return-v.errno}}function jd(r,a){try{return r=Tt.getStr(r),Tt.writeStat(a,M.stat(r))}catch(c){if(typeof M>"u"||c.name!=="ErrnoError")throw c;return-c.errno}}var qd=()=>xe("native code called abort()"),Zt=r=>{for(var a="";;){var c=tt[r++];if(!c)return a;a+=String.fromCharCode(c)}},pr={},Xi={},Ys={},es=class extends Error{constructor(a){super(a),this.name="BindingError"}},vt=r=>{throw new es(r)};function Yd(r,a,c={}){var u=a.name;if(r||vt(`type "${u}" must have a positive integer typeid pointer`),Xi.hasOwnProperty(r)){if(c.ignoreDuplicateRegistrations)return;vt(`Cannot register type '${u}' twice`)}if(Xi[r]=a,delete Ys[r],pr.hasOwnProperty(r)){var p=pr[r];delete pr[r],p.forEach(v=>v())}}function On(r,a,c={}){if(a.argPackAdvance===void 0)throw new TypeError("registerType registeredInstance requires argPackAdvance");return Yd(r,a,c)}var ih=(r,a,c)=>{switch(a){case 1:return c?u=>rt[u]:u=>tt[u];case 2:return c?u=>St[u>>1]:u=>Bt[u>>1];case 4:return c?u=>Ie[u>>2]:u=>Ue[u>>2];case 8:return c?u=>Dt[u>>3]:u=>Ct[u>>3];default:throw new TypeError(`invalid integer width (${a}): ${r}`)}},$i=r=>{if(r===null)return"null";var a=typeof r;return a==="object"||a==="array"||a==="function"?r.toString():""+r},rh=(r,a,c,u)=>{if(a<c||a>u)throw new TypeError(`Passing a number "${$i(a)}" from JS side to C/C++ side to an argument of type "${r}", which is outside the valid range [${c}, ${u}]!`)},Zd=(r,a,c,u,p)=>{a=Zt(a);let v=u===0n,E=C=>C;if(v){let C=c*8;E=N=>BigInt.asUintN(C,N),p=E(p)}On(r,{name:a,fromWireType:E,toWireType:(C,N)=>{if(typeof N=="number")N=BigInt(N);else if(typeof N!="bigint")throw new TypeError(`Cannot convert "${$i(N)}" to ${this.name}`);return rh(a,N,u,p),N},argPackAdvance:ti,readValueFromPointer:ih(a,c,!v),destructorFunction:null})},ti=8,Jd=(r,a,c,u)=>{a=Zt(a),On(r,{name:a,fromWireType:function(p){return!!p},toWireType:function(p,v){return v?c:u},argPackAdvance:ti,readValueFromPointer:function(p){return this.fromWireType(tt[p])},destructorFunction:null})},Kd=r=>({count:r.count,deleteScheduled:r.deleteScheduled,preservePointerOnDelete:r.preservePointerOnDelete,ptr:r.ptr,ptrType:r.ptrType,smartPtr:r.smartPtr,smartPtrType:r.smartPtrType}),vl=r=>{function a(c){return c.$$.ptrType.registeredClass.name}vt(a(r)+" instance already deleted")},yl=!1,sh=r=>{},Qd=r=>{r.smartPtr?r.smartPtrType.rawDestructor(r.smartPtr):r.ptrType.registeredClass.rawDestructor(r.ptr)},ah=r=>{r.count.value-=1;var a=r.count.value===0;a&&Qd(r)},oh=(r,a,c)=>{if(a===c)return r;if(c.baseClass===void 0)return null;var u=oh(r,a,c.baseClass);return u===null?null:c.downcast(u)},lh={},ef={},tf=(r,a)=>{for(a===void 0&&vt("ptr should not be undefined");r.baseClass;)a=r.upcast(a),r=r.baseClass;return a},nf=(r,a)=>(a=tf(r,a),ef[a]),rf=class extends Error{constructor(a){super(a),this.name="InternalError"}},Zs=r=>{throw new rf(r)},Js=(r,a)=>{(!a.ptrType||!a.ptr)&&Zs("makeClassHandle requires ptr and ptrType");var c=!!a.smartPtrType,u=!!a.smartPtr;return c!==u&&Zs("Both smartPtrType and smartPtr must be specified"),a.count={value:1},ts(Object.create(r,{$$:{value:a,writable:!0}}))};function ch(r){var a=this.getPointee(r);if(!a)return this.destructor(r),null;var c=nf(this.registeredClass,a);if(c!==void 0){if(c.$$.count.value===0)return c.$$.ptr=a,c.$$.smartPtr=r,c.clone();var u=c.clone();return this.destructor(r),u}function p(){return this.isSmartPointer?Js(this.registeredClass.instancePrototype,{ptrType:this.pointeeType,ptr:a,smartPtrType:this,smartPtr:r}):Js(this.registeredClass.instancePrototype,{ptrType:this,ptr:r})}var v=this.registeredClass.getActualType(a),E=lh[v];if(!E)return p.call(this);var C;this.isConst?C=E.constPointerType:C=E.pointerType;var N=oh(a,this.registeredClass,C.registeredClass);return N===null?p.call(this):this.isSmartPointer?Js(C.registeredClass.instancePrototype,{ptrType:C,ptr:N,smartPtrType:this,smartPtr:r}):Js(C.registeredClass.instancePrototype,{ptrType:C,ptr:N})}var ts=r=>typeof FinalizationRegistry>"u"?(ts=a=>a,r):(yl=new FinalizationRegistry(a=>{console.warn(a.leakWarning),ah(a.$$)}),ts=a=>{var c=a.$$,u=!!c.smartPtr;if(u){var p={$$:c},v=c.ptrType.registeredClass,E=new Error(`Embind found a leaked C++ instance ${v.name} <${Mi(c.ptr)}>.
We'll free it automatically in this case, but this functionality is not reliable across various environments.
Make sure to invoke .delete() manually once you're done with the instance instead.
Originally allocated`);"captureStackTrace"in Error&&Error.captureStackTrace(E,ch),p.leakWarning=E.stack.replace(/^Error: /,""),yl.register(a,p,a)}return a},sh=a=>yl.unregister(a),ts(r)),Ks=[],sf=()=>{for(;Ks.length;){var r=Ks.pop();r.$$.deleteScheduled=!1,r.delete()}},hh,af=()=>{let r=Qs.prototype;Object.assign(r,{isAliasOf(c){if(!(this instanceof Qs)||!(c instanceof Qs))return!1;var u=this.$$.ptrType.registeredClass,p=this.$$.ptr;c.$$=c.$$;for(var v=c.$$.ptrType.registeredClass,E=c.$$.ptr;u.baseClass;)p=u.upcast(p),u=u.baseClass;for(;v.baseClass;)E=v.upcast(E),v=v.baseClass;return u===v&&p===E},clone(){if(this.$$.ptr||vl(this),this.$$.preservePointerOnDelete)return this.$$.count.value+=1,this;var c=ts(Object.create(Object.getPrototypeOf(this),{$$:{value:Kd(this.$$)}}));return c.$$.count.value+=1,c.$$.deleteScheduled=!1,c},delete(){this.$$.ptr||vl(this),this.$$.deleteScheduled&&!this.$$.preservePointerOnDelete&&vt("Object already scheduled for deletion"),sh(this),ah(this.$$),this.$$.preservePointerOnDelete||(this.$$.smartPtr=void 0,this.$$.ptr=void 0)},isDeleted(){return!this.$$.ptr},deleteLater(){return this.$$.ptr||vl(this),this.$$.deleteScheduled&&!this.$$.preservePointerOnDelete&&vt("Object already scheduled for deletion"),Ks.push(this),Ks.length===1&&hh&&hh(sf),this.$$.deleteScheduled=!0,this}});let a=Symbol.dispose;a&&(r[a]=r.delete)};function Qs(){}var ea=(r,a)=>Object.defineProperty(a,"name",{value:r}),xl=(r,a,c)=>{if(r[a].overloadTable===void 0){var u=r[a];r[a]=function(...p){return r[a].overloadTable.hasOwnProperty(p.length)||vt(`Function '${c}' called with an invalid number of arguments (${p.length}) - expects one of (${r[a].overloadTable})!`),r[a].overloadTable[p.length].apply(this,p)},r[a].overloadTable=[],r[a].overloadTable[u.argCount]=u}},Sl=(r,a,c)=>{t.hasOwnProperty(r)?((c===void 0||t[r].overloadTable!==void 0&&t[r].overloadTable[c]!==void 0)&&vt(`Cannot register public name '${r}' twice`),xl(t,r,r),t[r].overloadTable.hasOwnProperty(c)&&vt(`Cannot register multiple overloads of a function with the same number of arguments (${c})!`),t[r].overloadTable[c]=a):(t[r]=a,t[r].argCount=c)},of=48,lf=57,cf=r=>{k(typeof r=="string"),r=r.replace(/[^a-zA-Z0-9_]/g,"$");var a=r.charCodeAt(0);return a>=of&&a<=lf?`_${r}`:r};function hf(r,a,c,u,p,v,E,C){this.name=r,this.constructor=a,this.instancePrototype=c,this.rawDestructor=u,this.baseClass=p,this.getActualType=v,this.upcast=E,this.downcast=C,this.pureVirtualFunctions=[]}var ta=(r,a,c)=>{for(;a!==c;)a.upcast||vt(`Expected null or instance of ${c.name}, got an instance of ${a.name}`),r=a.upcast(r),a=a.baseClass;return r};function uf(r,a){if(a===null)return this.isReference&&vt(`null is not a valid ${this.name}`),0;a.$$||vt(`Cannot pass "${$i(a)}" as a ${this.name}`),a.$$.ptr||vt(`Cannot pass deleted object as a pointer of type ${this.name}`);var c=a.$$.ptrType.registeredClass,u=ta(a.$$.ptr,c,this.registeredClass);return u}function df(r,a){var c;if(a===null)return this.isReference&&vt(`null is not a valid ${this.name}`),this.isSmartPointer?(c=this.rawConstructor(),r!==null&&r.push(this.rawDestructor,c),c):0;(!a||!a.$$)&&vt(`Cannot pass "${$i(a)}" as a ${this.name}`),a.$$.ptr||vt(`Cannot pass deleted object as a pointer of type ${this.name}`),!this.isConst&&a.$$.ptrType.isConst&&vt(`Cannot convert argument of type ${a.$$.smartPtrType?a.$$.smartPtrType.name:a.$$.ptrType.name} to parameter type ${this.name}`);var u=a.$$.ptrType.registeredClass;if(c=ta(a.$$.ptr,u,this.registeredClass),this.isSmartPointer)switch(a.$$.smartPtr===void 0&&vt("Passing raw pointer to smart pointer is illegal"),this.sharingPolicy){case 0:a.$$.smartPtrType===this?c=a.$$.smartPtr:vt(`Cannot convert argument of type ${a.$$.smartPtrType?a.$$.smartPtrType.name:a.$$.ptrType.name} to parameter type ${this.name}`);break;case 1:c=a.$$.smartPtr;break;case 2:if(a.$$.smartPtrType===this)c=a.$$.smartPtr;else{var p=a.clone();c=this.rawShare(c,Jt.toHandle(()=>p.delete())),r!==null&&r.push(this.rawDestructor,c)}break;default:vt("Unsupporting sharing policy")}return c}function ff(r,a){if(a===null)return this.isReference&&vt(`null is not a valid ${this.name}`),0;a.$$||vt(`Cannot pass "${$i(a)}" as a ${this.name}`),a.$$.ptr||vt(`Cannot pass deleted object as a pointer of type ${this.name}`),a.$$.ptrType.isConst&&vt(`Cannot convert argument of type ${a.$$.ptrType.name} to parameter type ${this.name}`);var c=a.$$.ptrType.registeredClass,u=ta(a.$$.ptr,c,this.registeredClass);return u}function na(r){return this.fromWireType(Ue[r>>2])}var pf=()=>{Object.assign(ia.prototype,{getPointee(r){return this.rawGetPointee&&(r=this.rawGetPointee(r)),r},destructor(r){this.rawDestructor?.(r)},argPackAdvance:ti,readValueFromPointer:na,fromWireType:ch})};function ia(r,a,c,u,p,v,E,C,N,$,ee){this.name=r,this.registeredClass=a,this.isReference=c,this.isConst=u,this.isSmartPointer=p,this.pointeeType=v,this.sharingPolicy=E,this.rawGetPointee=C,this.rawConstructor=N,this.rawShare=$,this.rawDestructor=ee,!p&&a.baseClass===void 0?u?(this.toWireType=uf,this.destructorFunction=null):(this.toWireType=ff,this.destructorFunction=null):this.toWireType=df}var uh=(r,a,c)=>{t.hasOwnProperty(r)||Zs("Replacing nonexistent public symbol"),t[r].overloadTable!==void 0&&c!==void 0?t[r].overloadTable[c]=a:(t[r]=a,t[r].argCount=c)},dh=[],ra,we=r=>{var a=dh[r];return a||(dh[r]=a=ra.get(r)),k(ra.get(r)==a,"JavaScript-side Wasm function table mirror is out of date!"),a},ni=(r,a,c=!1)=>{k(!c,"Async bindings are only supported with JSPI."),r=Zt(r);function u(){var v=we(a);return v}var p=u();return typeof p!="function"&&vt(`unknown function pointer with signature ${r}: ${a}`),p};class mf extends Error{}var fh=r=>{var a=Ih(r),c=Zt(a);return Xn(a),c},ji=(r,a)=>{var c=[],u={};function p(v){if(!u[v]&&!Xi[v]){if(Ys[v]){Ys[v].forEach(p);return}c.push(v),u[v]=!0}}throw a.forEach(p),new mf(`${r}: `+c.map(fh).join([", "]))},Wn=(r,a,c)=>{r.forEach(C=>Ys[C]=a);function u(C){var N=c(C);N.length!==r.length&&Zs("Mismatched type converter count");for(var $=0;$<r.length;++$)On(r[$],N[$])}var p=new Array(a.length),v=[],E=0;a.forEach((C,N)=>{Xi.hasOwnProperty(C)?p[N]=Xi[C]:(v.push(C),pr.hasOwnProperty(C)||(pr[C]=[]),pr[C].push(()=>{p[N]=Xi[C],++E,E===v.length&&u(p)}))}),v.length===0&&u(p)},gf=(r,a,c,u,p,v,E,C,N,$,ee,ue,pe)=>{ee=Zt(ee),v=ni(p,v),C&&=ni(E,C),$&&=ni(N,$),pe=ni(ue,pe);var ce=cf(ee);Sl(ce,function(){ji(`Cannot construct ${ee} due to unbound types`,[u])}),Wn([r,a,c],u?[u]:[],ve=>{ve=ve[0];var Qe,yt;u?(Qe=ve.registeredClass,yt=Qe.instancePrototype):yt=Qs.prototype;var ft=ea(ee,function(...Nt){if(Object.getPrototypeOf(this)!==kt)throw new es(`Use 'new' to construct ${ee}`);if(At.constructor_body===void 0)throw new es(`${ee} has no accessible constructor`);var Zi=At.constructor_body[Nt.length];if(Zi===void 0)throw new es(`Tried to invoke ctor of ${ee} with invalid number of parameters (${Nt.length}) - expected (${Object.keys(At.constructor_body).toString()}) parameters instead!`);return Zi.apply(this,Nt)}),kt=Object.create(yt,{constructor:{value:ft}});ft.prototype=kt;var At=new hf(ee,ft,kt,pe,Qe,v,C,$);At.baseClass&&(At.baseClass.__derivedClasses??=[],At.baseClass.__derivedClasses.push(At));var cn=new ia(ee,At,!0,!1,!1),Kt=new ia(ee+"*",At,!1,!1,!1),gn=new ia(ee+" const*",At,!1,!0,!1);return lh[r]={pointerType:Kt,constPointerType:gn},uh(ce,ft),[cn,Kt,gn]})},bl=r=>{for(;r.length;){var a=r.pop(),c=r.pop();c(a)}};function ph(r){for(var a=1;a<r.length;++a)if(r[a]!==null&&r[a].destructorFunction===void 0)return!0;return!1}function _f(r,a,c,u,p){if(r<a||r>c){var v=a==c?a:`${a} to ${c}`;p(`function ${u} called with ${r} arguments, expected ${v}`)}}function vf(r,a,c,u){var p=ph(r),v=r.length-2,E=[],C=["fn"];a&&C.push("thisWired");for(var N=0;N<v;++N)E.push(`arg${N}`),C.push(`arg${N}Wired`);E=E.join(","),C=C.join(",");var $=`return function (${E}) {
`;$+=`checkArgCount(arguments.length, minArgs, maxArgs, humanName, throwBindingError);
`,p&&($+=`var destructors = [];
`);var ee=p?"destructors":"null",ue=["humanName","throwBindingError","invoker","fn","runDestructors","retType","classParam"];a&&($+=`var thisWired = classParam['toWireType'](${ee}, this);
`);for(var N=0;N<v;++N)$+=`var arg${N}Wired = argType${N}['toWireType'](${ee}, arg${N});
`,ue.push(`argType${N}`);$+=(c||u?"var rv = ":"")+`invoker(${C});
`;var pe=c?"rv":"";if(p)$+=`runDestructors(destructors);
`;else for(var N=a?1:2;N<r.length;++N){var ce=N===1?"thisWired":"arg"+(N-2)+"Wired";r[N].destructorFunction!==null&&($+=`${ce}_dtor(${ce});
`,ue.push(`${ce}_dtor`))}return c&&($+=`var ret = retType['fromWireType'](rv);
return ret;
`),$+=`}
`,ue.push("checkArgCount","minArgs","maxArgs"),$=`if (arguments.length !== ${ue.length}){ throw new Error(humanName + "Expected ${ue.length} closure arguments " + arguments.length + " given."); }
${$}`,[ue,$]}function yf(r){for(var a=r.length-2,c=r.length-1;c>=2&&r[c].optional;--c)a--;return a}function sa(r,a,c,u,p,v){var E=a.length;E<2&&vt("argTypes array size mismatch! Must at least get return value and 'this' types!"),k(!v,"Async bindings are only supported with JSPI.");for(var C=a[1]!==null&&c!==null,N=ph(a),$=a[0].name!=="void",ee=E-2,ue=yf(a),pe=[r,vt,u,p,bl,a[0],a[1]],ce=0;ce<E-2;++ce)pe.push(a[ce+2]);if(!N)for(var ce=C?1:2;ce<a.length;++ce)a[ce].destructorFunction!==null&&pe.push(a[ce].destructorFunction);pe.push(_f,ue,ee);let[ve,Qe]=vf(a,C,$,v);var yt=new Function(...ve,Qe)(...pe);return ea(r,yt)}var aa=(r,a)=>{for(var c=[],u=0;u<r;u++)c.push(Ue[a+u*4>>2]);return c},Ml=r=>{r=r.trim();let a=r.indexOf("(");return a===-1?r:(k(r.endsWith(")"),"Parentheses for argument names should match."),r.slice(0,a))},xf=(r,a,c,u,p,v,E,C,N)=>{var $=aa(c,u);a=Zt(a),a=Ml(a),v=ni(p,v,C),Wn([],[r],ee=>{ee=ee[0];var ue=`${ee.name}.${a}`;function pe(){ji(`Cannot call ${ue} due to unbound types`,$)}a.startsWith("@@")&&(a=Symbol[a.substring(2)]);var ce=ee.registeredClass.constructor;return ce[a]===void 0?(pe.argCount=c-1,ce[a]=pe):(xl(ce,a,ue),ce[a].overloadTable[c-1]=pe),Wn([],$,ve=>{var Qe=[ve[0],null].concat(ve.slice(1)),yt=sa(ue,Qe,null,v,E,C);if(ce[a].overloadTable===void 0?(yt.argCount=c-1,ce[a]=yt):ce[a].overloadTable[c-1]=yt,ee.registeredClass.__derivedClasses)for(let ft of ee.registeredClass.__derivedClasses)ft.constructor.hasOwnProperty(a)||(ft.constructor[a]=yt);return[]}),[]})},Sf=(r,a,c,u,p,v)=>{k(a>0);var E=aa(a,c);p=ni(u,p);var C=[v],N=[];Wn([],[r],$=>{$=$[0];var ee=`constructor ${$.name}`;if($.registeredClass.constructor_body===void 0&&($.registeredClass.constructor_body=[]),$.registeredClass.constructor_body[a-1]!==void 0)throw new es(`Cannot register multiple constructors with identical number of parameters (${a-1}) for class '${$.name}'! Overload resolution is currently only performed using the parameter count, not actual type info!`);return $.registeredClass.constructor_body[a-1]=()=>{ji(`Cannot construct ${$.name} due to unbound types`,E)},Wn([],E,ue=>(ue.splice(1,0,null),$.registeredClass.constructor_body[a-1]=sa(ee,ue,null,p,v),[])),[]})},bf=(r,a,c,u,p,v,E,C,N,$)=>{var ee=aa(c,u);a=Zt(a),a=Ml(a),v=ni(p,v,N),Wn([],[r],ue=>{ue=ue[0];var pe=`${ue.name}.${a}`;a.startsWith("@@")&&(a=Symbol[a.substring(2)]),C&&ue.registeredClass.pureVirtualFunctions.push(a);function ce(){ji(`Cannot call ${pe} due to unbound types`,ee)}var ve=ue.registeredClass.instancePrototype,Qe=ve[a];return Qe===void 0||Qe.overloadTable===void 0&&Qe.className!==ue.name&&Qe.argCount===c-2?(ce.argCount=c-2,ce.className=ue.name,ve[a]=ce):(xl(ve,a,pe),ve[a].overloadTable[c-2]=ce),Wn([],ee,yt=>{var ft=sa(pe,yt,ue,v,E,N);return ve[a].overloadTable===void 0?(ft.argCount=c-2,ve[a]=ft):ve[a].overloadTable[c-2]=ft,[]}),[]})},mh=(r,a,c)=>(r instanceof Object||vt(`${c} with invalid "this": ${r}`),r instanceof a.registeredClass.constructor||vt(`${c} incompatible with "this" of type ${r.constructor.name}`),r.$$.ptr||vt(`cannot call emscripten binding method ${c} on deleted object`),ta(r.$$.ptr,r.$$.ptrType.registeredClass,a.registeredClass)),Mf=(r,a,c,u,p,v,E,C,N,$)=>{a=Zt(a),p=ni(u,p),Wn([],[r],ee=>{ee=ee[0];var ue=`${ee.name}.${a}`,pe={get(){ji(`Cannot access ${ue} due to unbound types`,[c,E])},enumerable:!0,configurable:!0};return N?pe.set=()=>ji(`Cannot access ${ue} due to unbound types`,[c,E]):pe.set=ce=>vt(ue+" is a read-only property"),Object.defineProperty(ee.registeredClass.instancePrototype,a,pe),Wn([],N?[c,E]:[c],ce=>{var ve=ce[0],Qe={get(){var ft=mh(this,ee,ue+" getter");return ve.fromWireType(p(v,ft))},enumerable:!0};if(N){N=ni(C,N);var yt=ce[1];Qe.set=function(ft){var kt=mh(this,ee,ue+" setter"),At=[];N($,kt,yt.toWireType(At,ft)),bl(At)}}return Object.defineProperty(ee.registeredClass.instancePrototype,a,Qe),[]}),[]})},Ef=(r,a,c)=>{r=Zt(r),Wn([],[a],u=>(u=u[0],t[r]=u.fromWireType(c),[]))},gh=[],ii=[0,1,,1,null,1,!0,1,!1,1],El=r=>{r>9&&--ii[r+1]===0&&(k(ii[r]!==void 0,"Decref for unallocated handle."),ii[r]=void 0,gh.push(r))},Jt={toValue:r=>(r||vt(`Cannot use deleted val. handle = ${r}`),k(r===2||ii[r]!==void 0&&r%2===0,`invalid handle: ${r}`),ii[r]),toHandle:r=>{switch(r){case void 0:return 2;case null:return 4;case!0:return 6;case!1:return 8;default:{let a=gh.pop()||ii.length;return ii[a]=r,ii[a+1]=1,a}}}},_h={name:"emscripten::val",fromWireType:r=>{var a=Jt.toValue(r);return El(r),a},toWireType:(r,a)=>Jt.toHandle(a),argPackAdvance:ti,readValueFromPointer:na,destructorFunction:null},vh=r=>On(r,_h),wf=(r,a,c)=>{switch(a){case 1:return c?function(u){return this.fromWireType(rt[u])}:function(u){return this.fromWireType(tt[u])};case 2:return c?function(u){return this.fromWireType(St[u>>1])}:function(u){return this.fromWireType(Bt[u>>1])};case 4:return c?function(u){return this.fromWireType(Ie[u>>2])}:function(u){return this.fromWireType(Ue[u>>2])};default:throw new TypeError(`invalid integer width (${a}): ${r}`)}},Tf=(r,a,c,u)=>{a=Zt(a);function p(){}p.values={},On(r,{name:a,constructor:p,fromWireType:function(v){return this.constructor.values[v]},toWireType:(v,E)=>E.value,argPackAdvance:ti,readValueFromPointer:wf(a,c,u),destructorFunction:null}),Sl(a,p)},oa=(r,a)=>{var c=Xi[r];return c===void 0&&vt(`${a} has unknown type ${fh(r)}`),c},Af=(r,a,c)=>{var u=oa(r,"enum");a=Zt(a);var p=u.constructor,v=Object.create(u.constructor.prototype,{value:{value:c},constructor:{value:ea(`${u.name}_${a}`,function(){})}});p.values[c]=v,p[a]=v},Cf=(r,a)=>{switch(a){case 4:return function(c){return this.fromWireType(Vt[c>>2])};case 8:return function(c){return this.fromWireType(W[c>>3])};default:throw new TypeError(`invalid float width (${a}): ${r}`)}},Rf=(r,a,c)=>{a=Zt(a),On(r,{name:a,fromWireType:u=>u,toWireType:(u,p)=>{if(typeof p!="number"&&typeof p!="boolean")throw new TypeError(`Cannot convert ${$i(p)} to ${this.name}`);return p},argPackAdvance:ti,readValueFromPointer:Cf(a,c),destructorFunction:null})},Pf=(r,a,c,u,p,v,E,C)=>{var N=aa(a,c);r=Zt(r),r=Ml(r),p=ni(u,p,E),Sl(r,function(){ji(`Cannot call ${r} due to unbound types`,N)},a-1),Wn([],N,$=>{var ee=[$[0],null].concat($.slice(1));return uh(r,sa(r,ee,null,p,v,E),a-1),[]})},If=(r,a,c,u,p)=>{a=Zt(a);let v=u===0,E=N=>N;if(v){var C=32-8*c;E=N=>N<<C>>>C,p=E(p)}On(r,{name:a,fromWireType:E,toWireType:(N,$)=>{if(typeof $!="number"&&typeof $!="boolean")throw new TypeError(`Cannot convert "${$i($)}" to ${a}`);return rh(a,$,u,p),$},argPackAdvance:ti,readValueFromPointer:ih(a,c,u!==0),destructorFunction:null})},Df=(r,a,c)=>{var u=[Int8Array,Uint8Array,Int16Array,Uint16Array,Int32Array,Uint32Array,Float32Array,Float64Array,BigInt64Array,BigUint64Array],p=u[a];function v(E){var C=Ue[E>>2],N=Ue[E+4>>2];return new p(rt.buffer,N,C)}c=Zt(c),On(r,{name:c,fromWireType:v,argPackAdvance:ti,readValueFromPointer:v},{ignoreDuplicateRegistrations:!0})},Lf=Object.assign({optional:!0},_h),Ff=(r,a)=>{On(r,Lf)},qi=(r,a,c)=>(k(typeof c=="number","stringToUTF8(str, outPtr, maxBytesToWrite) is missing the third parameter that specifies the length of the output buffer!"),Ge(r,tt,a,c)),Nf=(r,a)=>{a=Zt(a);var c=!0;On(r,{name:a,fromWireType(u){var p=Ue[u>>2],v=u+4,E;if(c)for(var C=v,N=0;N<=p;++N){var $=v+N;if(N==p||tt[$]==0){var ee=$-C,ue=An(C,ee);E===void 0?E=ue:(E+="\0",E+=ue),C=$+1}}else{for(var pe=new Array(p),N=0;N<p;++N)pe[N]=String.fromCharCode(tt[v+N]);E=pe.join("")}return Xn(u),E},toWireType(u,p){p instanceof ArrayBuffer&&(p=new Uint8Array(p));var v,E=typeof p=="string";E||ArrayBuffer.isView(p)&&p.BYTES_PER_ELEMENT==1||vt("Cannot pass non-string to std::string"),c&&E?v=ct(p):v=p.length;var C=Cl(4+v+1),N=C+4;if(Ue[C>>2]=v,E)if(c)qi(p,N,v+1);else for(var $=0;$<v;++$){var ee=p.charCodeAt($);ee>255&&(Xn(C),vt("String has UTF-16 code units that do not fit in 8 bits")),tt[N+$]=ee}else tt.set(p,N);return u!==null&&u.push(Xn,C),C},argPackAdvance:ti,readValueFromPointer:na,destructorFunction(u){Xn(u)}})},yh=typeof TextDecoder<"u"?new TextDecoder("utf-16le"):void 0,Uf=(r,a)=>{k(r%2==0,"Pointer passed to UTF16ToString must be aligned to two bytes!");for(var c=r>>1,u=c+a/2,p=c;!(p>=u)&&Bt[p];)++p;if(p-c>16&&yh)return yh.decode(Bt.subarray(c,p));for(var v="",E=c;!(E>=u);++E){var C=Bt[E];if(C==0)break;v+=String.fromCharCode(C)}return v},Of=(r,a,c)=>{if(k(a%2==0,"Pointer passed to stringToUTF16 must be aligned to two bytes!"),k(typeof c=="number","stringToUTF16(str, outPtr, maxBytesToWrite) is missing the third parameter that specifies the length of the output buffer!"),c??=2147483647,c<2)return 0;c-=2;for(var u=a,p=c<r.length*2?c/2:r.length,v=0;v<p;++v){var E=r.charCodeAt(v);St[a>>1]=E,a+=2}return St[a>>1]=0,a-u},Bf=r=>r.length*2,kf=(r,a)=>{k(r%4==0,"Pointer passed to UTF32ToString must be aligned to four bytes!");for(var c="",u=0;!(u>=a/4);u++){var p=Ie[r+u*4>>2];if(!p)break;c+=String.fromCodePoint(p)}return c},zf=(r,a,c)=>{if(k(a%4==0,"Pointer passed to stringToUTF32 must be aligned to four bytes!"),k(typeof c=="number","stringToUTF32(str, outPtr, maxBytesToWrite) is missing the third parameter that specifies the length of the output buffer!"),c??=2147483647,c<4)return 0;for(var u=a,p=u+c-4,v=0;v<r.length;++v){var E=r.codePointAt(v);if(E>65535&&v++,Ie[a>>2]=E,a+=4,a+4>p)break}return Ie[a>>2]=0,a-u},Vf=r=>{for(var a=0,c=0;c<r.length;++c){var u=r.codePointAt(c);u>65535&&c++,a+=4}return a},Gf=(r,a,c)=>{c=Zt(c);var u,p,v,E;a===2?(u=Uf,p=Of,E=Bf,v=C=>Bt[C>>1]):a===4&&(u=kf,p=zf,E=Vf,v=C=>Ue[C>>2]),On(r,{name:c,fromWireType:C=>{for(var N=Ue[C>>2],$,ee=C+4,ue=0;ue<=N;++ue){var pe=C+4+ue*a;if(ue==N||v(pe)==0){var ce=pe-ee,ve=u(ee,ce);$===void 0?$=ve:($+="\0",$+=ve),ee=pe+a}}return Xn(C),$},toWireType:(C,N)=>{typeof N!="string"&&vt(`Cannot pass non-string to C++ string type ${c}`);var $=E(N),ee=Cl(4+$+a);return Ue[ee>>2]=$/a,p(N,ee+4,$+a),C!==null&&C.push(Xn,ee),ee},argPackAdvance:ti,readValueFromPointer:na,destructorFunction(C){Xn(C)}})},Hf=(r,a)=>{vh(r)},Wf=(r,a)=>{a=Zt(a),On(r,{isVoid:!0,name:a,argPackAdvance:0,fromWireType:()=>{},toWireType:(c,u)=>{}})},Xf=()=>{throw new ge},xh=(r,a,c)=>{var u=[],p=r.toWireType(u,c);return u.length&&(Ue[a>>2]=Jt.toHandle(u)),p},$f=(r,a,c)=>(r=Jt.toValue(r),a=oa(a,"emval::as"),xh(a,c,r)),la=[],jf=(r,a,c,u)=>(r=la[r],a=Jt.toValue(a),r(null,a,c,u)),qf={},wl=r=>{var a=qf[r];return a===void 0?Zt(r):a},Yf=(r,a,c,u,p)=>(r=la[r],a=Jt.toValue(a),c=wl(c),r(a,a[c],u,p)),Sh=()=>globalThis,Zf=r=>r===0?Jt.toHandle(Sh()):(r=wl(r),Jt.toHandle(Sh()[r])),Jf=r=>{var a=la.length;return la.push(r),a},Kf=(r,a)=>{for(var c=new Array(r),u=0;u<r;++u)c[u]=oa(Ue[a+u*4>>2],`parameter ${u}`);return c},Qf=(r,a,c)=>{var u=Kf(r,a),p=u.shift();r--;var v=`return function (obj, func, destructorsRef, args) {
`,E=0,C=[];c===0&&C.push("obj");for(var N=["retType"],$=[p],ee=0;ee<r;++ee)C.push(`arg${ee}`),N.push(`argType${ee}`),$.push(u[ee]),v+=`  var arg${ee} = argType${ee}.readValueFromPointer(args${E?"+"+E:""});
`,E+=u[ee].argPackAdvance;var ue=c===1?"new func":"func.call";v+=`  var rv = ${ue}(${C.join(", ")});
`,p.isVoid||(N.push("emval_returnValue"),$.push(xh),v+=`  return emval_returnValue(retType, destructorsRef, rv);
`),v+=`};
`;var pe=new Function(...N,v)(...$),ce=`methodCaller<(${u.map(ve=>ve.name).join(", ")}) => ${p.name}>`;return Jf(ea(ce,pe))},ep=(r,a)=>(r=Jt.toValue(r),a=Jt.toValue(a),Jt.toHandle(r[a])),tp=r=>{r>9&&(ii[r+1]+=1)},np=r=>(r=Jt.toValue(r),typeof r=="number"),ip=r=>(r=Jt.toValue(r),typeof r=="string"),rp=()=>Jt.toHandle([]),sp=r=>Jt.toHandle(wl(r)),ap=r=>{var a=Jt.toValue(r);bl(a),El(r)},op=(r,a)=>{r=oa(r,"_emval_take_value");var c=r.readValueFromPointer(a);return Jt.toHandle(c)},lp=r=>{throw r=Jt.toValue(r),r},cp=r=>r%4===0&&(r%100!==0||r%400===0),hp=[0,31,60,91,121,152,182,213,244,274,305,335],up=[0,31,59,90,120,151,181,212,243,273,304,334],bh=r=>{var a=cp(r.getFullYear()),c=a?hp:up,u=c[r.getMonth()]+r.getDate()-1;return u},dp=9007199254740992,fp=-9007199254740992,Tl=r=>r<fp||r>dp?NaN:Number(r);function pp(r,a){r=Tl(r);var c=new Date(r*1e3);Ie[a>>2]=c.getSeconds(),Ie[a+4>>2]=c.getMinutes(),Ie[a+8>>2]=c.getHours(),Ie[a+12>>2]=c.getDate(),Ie[a+16>>2]=c.getMonth(),Ie[a+20>>2]=c.getFullYear()-1900,Ie[a+24>>2]=c.getDay();var u=bh(c)|0;Ie[a+28>>2]=u,Ie[a+36>>2]=-(c.getTimezoneOffset()*60);var p=new Date(c.getFullYear(),0,1),v=new Date(c.getFullYear(),6,1).getTimezoneOffset(),E=p.getTimezoneOffset(),C=(v!=E&&c.getTimezoneOffset()==Math.min(E,v))|0;Ie[a+32>>2]=C}var mp=function(r){var a=(()=>{var c=new Date(Ie[r+20>>2]+1900,Ie[r+16>>2],Ie[r+12>>2],Ie[r+8>>2],Ie[r+4>>2],Ie[r>>2],0),u=Ie[r+32>>2],p=c.getTimezoneOffset(),v=new Date(c.getFullYear(),0,1),E=new Date(c.getFullYear(),6,1).getTimezoneOffset(),C=v.getTimezoneOffset(),N=Math.min(C,E);if(u<0)Ie[r+32>>2]=+(E!=C&&N==p);else if(u>0!=(N==p)){var $=Math.max(C,E),ee=u>0?N:$;c.setTime(c.getTime()+(ee-p)*6e4)}Ie[r+24>>2]=c.getDay();var ue=bh(c)|0;Ie[r+28>>2]=ue,Ie[r>>2]=c.getSeconds(),Ie[r+4>>2]=c.getMinutes(),Ie[r+8>>2]=c.getHours(),Ie[r+12>>2]=c.getDate(),Ie[r+16>>2]=c.getMonth(),Ie[r+20>>2]=c.getYear();var pe=c.getTime();return isNaN(pe)?-1:pe/1e3})();return BigInt(a)},gp=(r,a,c,u)=>{var p=new Date().getFullYear(),v=new Date(p,0,1),E=new Date(p,6,1),C=v.getTimezoneOffset(),N=E.getTimezoneOffset(),$=Math.max(C,N);Ue[r>>2]=$*60,Ie[a>>2]=+(C!=N);var ee=ce=>{var ve=ce>=0?"-":"+",Qe=Math.abs(ce),yt=String(Math.floor(Qe/60)).padStart(2,"0"),ft=String(Qe%60).padStart(2,"0");return`UTC${ve}${yt}${ft}`},ue=ee(C),pe=ee(N);k(ue),k(pe),k(ct(ue)<=16,`timezone name truncated to fit in TZNAME_MAX (${ue})`),k(ct(pe)<=16,`timezone name truncated to fit in TZNAME_MAX (${pe})`),N<C?(qi(ue,c,17),qi(pe,u,17)):(qi(ue,u,17),qi(pe,c,17))},Mh=()=>performance.now(),Eh=()=>Date.now(),_p=1,vp=r=>r>=0&&r<=3;function yp(r,a,c){if(a=Tl(a),!vp(r))return 28;var u;if(r===0)u=Eh();else if(_p)u=Mh();else return 52;var p=Math.round(u*1e3*1e3);return Dt[c>>3]=BigInt(p),0}var ca=[],xp=(r,a)=>{k(Array.isArray(ca)),k(a%16==0),ca.length=0;for(var c;c=tt[r++];){var u=String.fromCharCode(c),p=["d","f","i","p"];p.push("j"),k(p.includes(u),`Invalid character ${c}("${u}") in readEmAsmArgs! Use only [${p}], and do not specify "v" for void return argument.`);var v=c!=105;v&=c!=112,a+=v&&a%8?4:0,ca.push(c==112?Ue[a>>2]:c==106?Dt[a>>3]:c==105?Ie[a>>2]:W[a>>3]),a+=v?8:4}return ca},Sp=(r,a,c)=>{var u=xp(a,c);return k(Ph.hasOwnProperty(r),`No EM_ASM constant found at address ${r}.  The loaded WebAssembly file is likely out of sync with the generated JavaScript.`),Ph[r](...u)},bp=(r,a,c)=>Sp(r,a,c),wh=()=>2147483648,Mp=()=>wh(),Ep=(r,a)=>(k(a,"alignment argument is required"),Math.ceil(r/a)*a),wp=r=>{var a=gt.buffer,c=(r-a.byteLength+65535)/65536|0;try{return gt.grow(c),x(),1}catch(u){R(`growMemory: Attempted to grow heap from ${a.byteLength} bytes to ${r} bytes, but got error: ${u}`)}},Tp=r=>{var a=tt.length;r>>>=0,k(r>a);var c=wh();if(r>c)return R(`Cannot enlarge memory, requested ${r} bytes, but the limit is ${c} bytes!`),!1;for(var u=1;u<=4;u*=2){var p=a*(1+.2/u);p=Math.min(p,r+100663296);var v=Math.min(c,Ep(Math.max(r,p),65536)),E=wp(v);if(E)return!0}return R(`Failed to grow the heap from ${a} bytes to ${v} bytes, not enough memory!`),!1},Al={},Ap=()=>f||"./this.program",ns=()=>{if(!ns.strings){var r=(typeof navigator=="object"&&navigator.language||"C").replace("-","_")+".UTF-8",a={USER:"web_user",LOGNAME:"web_user",PATH:"/",PWD:"/",HOME:"/home/web_user",LANG:r,_:Ap()};for(var c in Al)Al[c]===void 0?delete a[c]:a[c]=Al[c];var u=[];for(var c in a)u.push(`${c}=${a[c]}`);ns.strings=u}return ns.strings},Cp=(r,a)=>{var c=0,u=0;for(var p of ns()){var v=a+c;Ue[r+u>>2]=v,c+=qi(p,v,1/0)+1,u+=4}return 0},Rp=(r,a)=>{var c=ns();Ue[r>>2]=c.length;var u=0;for(var p of c)u+=ct(p)+1;return Ue[a>>2]=u,0},Th=0,Ah=()=>Ws||Th>0,Pp=r=>{te=r,Ah()||(t.onExit?.(r),H=!0),g(r,new me(r))},Ip=(r,a)=>{if(te=r,Hg(),Ah()&&!a){var c=`program exited (with status: ${r}), but keepRuntimeAlive() is set (counter=${Th}) due to an async operation, so halting execution but not exiting the runtime or preventing further async execution (you can use emscripten_force_exit, if you want to force a true shutdown)`;dt?.(c),R(c)}Pp(r)},Dp=Ip;function Lp(r){try{var a=Tt.getStreamFromFD(r);return M.close(a),0}catch(c){if(typeof M>"u"||c.name!=="ErrnoError")throw c;return c.errno}}var Fp=(r,a,c,u)=>{for(var p=0,v=0;v<c;v++){var E=Ue[a>>2],C=Ue[a+4>>2];a+=8;var N=M.read(r,rt,E,C,u);if(N<0)return-1;if(p+=N,N<C)break;typeof u<"u"&&(u+=N)}return p};function Np(r,a,c,u){try{var p=Tt.getStreamFromFD(r),v=Fp(p,a,c);return Ue[u>>2]=v,0}catch(E){if(typeof M>"u"||E.name!=="ErrnoError")throw E;return E.errno}}function Up(r,a,c,u){a=Tl(a);try{if(isNaN(a))return 61;var p=Tt.getStreamFromFD(r);return M.llseek(p,a,c),Dt[u>>3]=BigInt(p.position),p.getdents&&a===0&&c===0&&(p.getdents=null),0}catch(v){if(typeof M>"u"||v.name!=="ErrnoError")throw v;return v.errno}}var Op=(r,a,c,u)=>{for(var p=0,v=0;v<c;v++){var E=Ue[a>>2],C=Ue[a+4>>2];a+=8;var N=M.write(r,rt,E,C,u);if(N<0)return-1;if(p+=N,N<C)break;typeof u<"u"&&(u+=N)}return p};function Bp(r,a,c,u){try{var p=Tt.getStreamFromFD(r),v=Op(p,a,c);return Ue[u>>2]=v,0}catch(E){if(typeof M>"u"||E.name!=="ErrnoError")throw E;return E.errno}}var kp=r=>r,zp=r=>{var a=t["_"+r];return k(a,"Cannot call unknown function "+r+", make sure it is exported"),a},Vp=(r,a)=>{k(r.length>=0,"writeArrayToMemory array must have a length (should be an array or typed array)"),rt.set(r,a)},ha=r=>Uh(r),Gp=r=>{var a=ct(r)+1,c=ha(a);return qi(r,c,a),c},Ch=(r,a,c,u,p)=>{var v={string:ve=>{var Qe=0;return ve!=null&&ve!==0&&(Qe=Gp(ve)),Qe},array:ve=>{var Qe=ha(ve.length);return Vp(ve,Qe),Qe}};function E(ve){return a==="string"?An(ve):a==="boolean"?!!ve:ve}var C=zp(r),N=[],$=0;if(k(a!=="array",'Return type should not be "array".'),u)for(var ee=0;ee<u.length;ee++){var ue=v[c[ee]];ue?($===0&&($=Se()),N[ee]=ue(u[ee])):N[ee]=u[ee]}var pe=C(...N);function ce(ve){return $!==0&&ye($),E(ve)}return pe=ce(pe),pe},Hp=(r,a,c,u)=>(...p)=>Ch(r,a,c,p,u),Wp=(...r)=>M.createPath(...r),Xp=(...r)=>M.unlink(...r),$p=(...r)=>M.createLazyFile(...r),jp=(...r)=>M.createDevice(...r),qp=r=>ua(r),Yp=r=>Il(r),Zp=r=>{var a=Se(),c=ha(4),u=ha(4);Bh(r,c,u);var p=Ue[c>>2],v=Ue[u>>2],E=An(p);Xn(p);var C;return v&&(C=An(v),Xn(v)),ye(a),[E,C]},Rh=r=>Zp(r);M.createPreloadedFile=Gn,M.staticInit(),af(),pf(),k(ii.length===10),t.noExitRuntime&&(Ws=t.noExitRuntime),t.preloadPlugins&&(mn=t.preloadPlugins),t.print&&(z=t.print),t.printErr&&(R=t.printErr),t.wasmBinary&&(J=t.wasmBinary),Qp(),t.arguments&&(d=t.arguments),t.thisProgram&&(f=t.thisProgram),k(typeof t.memoryInitializerPrefixURL>"u","Module.memoryInitializerPrefixURL option was removed, use Module.locateFile instead"),k(typeof t.pthreadMainPrefixURL>"u","Module.pthreadMainPrefixURL option was removed, use Module.locateFile instead"),k(typeof t.cdInitializerPrefixURL>"u","Module.cdInitializerPrefixURL option was removed, use Module.locateFile instead"),k(typeof t.filePackagePrefixURL>"u","Module.filePackagePrefixURL option was removed, use Module.locateFile instead"),k(typeof t.read>"u","Module.read option was removed"),k(typeof t.readAsync>"u","Module.readAsync option was removed (modify readAsync in JS)"),k(typeof t.readBinary>"u","Module.readBinary option was removed (modify readBinary in JS)"),k(typeof t.setWindowTitle>"u","Module.setWindowTitle option was removed (modify emscripten_set_window_title in JS)"),k(typeof t.TOTAL_MEMORY>"u","Module.TOTAL_MEMORY has been renamed Module.INITIAL_MEMORY"),k(typeof t.ENVIRONMENT>"u","Module.ENVIRONMENT has been deprecated. To force the environment, use the ENVIRONMENT compile-time option (for example, -sENVIRONMENT=web or -sENVIRONMENT=node)"),k(typeof t.STACK_SIZE>"u","STACK_SIZE can no longer be set at runtime.  Use -sSTACK_SIZE at link time"),k(typeof t.wasmMemory>"u","Use of `wasmMemory` detected.  Use -sIMPORTED_MEMORY to define wasmMemory externally"),k(typeof t.INITIAL_MEMORY>"u","Detected runtime INITIAL_MEMORY setting.  Use -sIMPORTED_MEMORY to define wasmMemory dynamically"),t.addRunDependency=Ce,t.removeRunDependency=Xe,t.ccall=Ch,t.cwrap=Hp,t.FS_createPreloadedFile=Gn,t.FS_unlink=Xp,t.FS_createPath=Wp,t.FS_createDevice=jp,t.FS=M,t.FS_createDataFile=rn,t.FS_createLazyFile=$p,t.MEMFS=qe;var Jp=["writeI53ToI64","writeI53ToI64Clamped","writeI53ToI64Signaling","writeI53ToU64Clamped","writeI53ToU64Signaling","readI53FromI64","readI53FromU64","convertI32PairToI53","convertI32PairToI53Checked","convertU32PairToI53","getTempRet0","zeroMemory","withStackSave","inetPton4","inetNtop4","inetPton6","inetNtop6","readSockaddr","writeSockaddr","emscriptenLog","runMainThreadEmAsm","jstoi_q","autoResumeAudioContext","getDynCaller","dynCall","handleException","runtimeKeepalivePush","runtimeKeepalivePop","callUserCallback","maybeExit","asmjsMangle","HandleAllocator","getNativeTypeSize","addOnInit","addOnPostCtor","addOnPreMain","addOnExit","STACK_SIZE","STACK_ALIGN","POINTER_SIZE","ASSERTIONS","uleb128Encode","sigToWasmTypes","generateFuncType","convertJsFunctionToWasm","getEmptyTableSlot","updateTableMap","getFunctionAddress","addFunction","removeFunction","reallyNegative","unSign","strLen","reSign","formatString","intArrayToString","stringToAscii","stringToNewUTF8","registerKeyEventCallback","maybeCStringToJsString","findEventTarget","getBoundingClientRect","fillMouseEventData","registerMouseEventCallback","registerWheelEventCallback","registerUiEventCallback","registerFocusEventCallback","fillDeviceOrientationEventData","registerDeviceOrientationEventCallback","fillDeviceMotionEventData","registerDeviceMotionEventCallback","screenOrientation","fillOrientationChangeEventData","registerOrientationChangeEventCallback","fillFullscreenChangeEventData","registerFullscreenChangeEventCallback","JSEvents_requestFullscreen","JSEvents_resizeCanvasForFullscreen","registerRestoreOldStyle","hideEverythingExceptGivenElement","restoreHiddenElements","setLetterbox","softFullscreenResizeWebGLRenderTarget","doRequestFullscreen","fillPointerlockChangeEventData","registerPointerlockChangeEventCallback","registerPointerlockErrorEventCallback","requestPointerLock","fillVisibilityChangeEventData","registerVisibilityChangeEventCallback","registerTouchEventCallback","fillGamepadEventData","registerGamepadEventCallback","registerBeforeUnloadEventCallback","fillBatteryEventData","battery","registerBatteryEventCallback","setCanvasElementSize","getCanvasElementSize","jsStackTrace","getCallstack","convertPCtoSourceLocation","wasiRightsToMuslOFlags","wasiOFlagsToMuslOFlags","safeSetTimeout","setImmediateWrapped","safeRequestAnimationFrame","clearImmediateWrapped","registerPostMainLoop","registerPreMainLoop","getPromise","makePromise","idsToPromises","makePromiseCallback","Browser_asyncPrepareDataCounter","arraySum","addDays","getSocketFromFD","getSocketAddress","FS_mkdirTree","_setNetworkCallback","heapObjectForWebGLType","toTypedArrayIndex","webgl_enable_ANGLE_instanced_arrays","webgl_enable_OES_vertex_array_object","webgl_enable_WEBGL_draw_buffers","webgl_enable_WEBGL_multi_draw","webgl_enable_EXT_polygon_offset_clamp","webgl_enable_EXT_clip_control","webgl_enable_WEBGL_polygon_mode","emscriptenWebGLGet","computeUnpackAlignedImageSize","colorChannelsInGlTextureFormat","emscriptenWebGLGetTexPixelData","emscriptenWebGLGetUniform","webglGetUniformLocation","webglPrepareUniformLocationsBeforeFirstUse","webglGetLeftBracePos","emscriptenWebGLGetVertexAttrib","__glGetActiveAttribOrUniform","writeGLArray","registerWebGlEventCallback","runAndAbortIfError","ALLOC_NORMAL","ALLOC_STACK","allocate","writeStringToMemory","writeAsciiToMemory","demangle","stackTrace","getFunctionArgsName","createJsInvokerSignature","PureVirtualError","registerInheritedInstance","unregisterInheritedInstance","getInheritedInstanceCount","getLiveInheritedInstances","setDelayFunction","count_emval_handles"];Jp.forEach(Be);var Kp=["run","out","err","callMain","abort","wasmMemory","wasmExports","HEAPF32","HEAPF64","HEAP8","HEAPU8","HEAP16","HEAPU16","HEAP32","HEAPU32","HEAP64","HEAPU64","writeStackCookie","checkStackCookie","INT53_MAX","INT53_MIN","bigintToI53Checked","stackSave","stackRestore","stackAlloc","setTempRet0","ptrToString","exitJS","getHeapMax","growMemory","ENV","ERRNO_CODES","strError","DNS","Protocols","Sockets","timers","warnOnce","readEmAsmArgsArray","readEmAsmArgs","runEmAsmFunction","getExecutableName","keepRuntimeAlive","asyncLoad","alignMemory","mmapAlloc","wasmTable","getUniqueRunDependency","noExitRuntime","addOnPreRun","addOnPostRun","freeTableIndexes","functionsInTableMap","setValue","getValue","PATH","PATH_FS","UTF8Decoder","UTF8ArrayToString","UTF8ToString","stringToUTF8Array","stringToUTF8","lengthBytesUTF8","intArrayFromString","AsciiToString","UTF16Decoder","UTF16ToString","stringToUTF16","lengthBytesUTF16","UTF32ToString","stringToUTF32","lengthBytesUTF32","stringToUTF8OnStack","writeArrayToMemory","JSEvents","specialHTMLTargets","findCanvasEventTarget","currentFullscreenStrategy","restoreOldWindowedStyle","UNWIND_CACHE","ExitStatus","getEnvStrings","checkWasiClock","doReadv","doWritev","initRandomFill","randomFill","emSetImmediate","emClearImmediate_deps","emClearImmediate","promiseMap","uncaughtExceptionCount","exceptionLast","exceptionCaught","ExceptionInfo","findMatchingCatch","getExceptionMessageCommon","Browser","requestFullscreen","requestFullScreen","setCanvasSize","getUserMedia","createContext","getPreloadedImageData__data","wget","MONTH_DAYS_REGULAR","MONTH_DAYS_LEAP","MONTH_DAYS_REGULAR_CUMULATIVE","MONTH_DAYS_LEAP_CUMULATIVE","isLeapYear","ydayFromDate","SYSCALLS","preloadPlugins","FS_modeStringToFlags","FS_getMode","FS_stdin_getChar_buffer","FS_stdin_getChar","FS_readFile","FS_root","FS_mounts","FS_devices","FS_streams","FS_nextInode","FS_nameTable","FS_currentPath","FS_initialized","FS_ignorePermissions","FS_filesystems","FS_syncFSRequests","FS_readFiles","FS_lookupPath","FS_getPath","FS_hashName","FS_hashAddNode","FS_hashRemoveNode","FS_lookupNode","FS_createNode","FS_destroyNode","FS_isRoot","FS_isMountpoint","FS_isFile","FS_isDir","FS_isLink","FS_isChrdev","FS_isBlkdev","FS_isFIFO","FS_isSocket","FS_flagsToPermissionString","FS_nodePermissions","FS_mayLookup","FS_mayCreate","FS_mayDelete","FS_mayOpen","FS_checkOpExists","FS_nextfd","FS_getStreamChecked","FS_getStream","FS_createStream","FS_closeStream","FS_dupStream","FS_doSetAttr","FS_chrdev_stream_ops","FS_major","FS_minor","FS_makedev","FS_registerDevice","FS_getDevice","FS_getMounts","FS_syncfs","FS_mount","FS_unmount","FS_lookup","FS_mknod","FS_statfs","FS_statfsStream","FS_statfsNode","FS_create","FS_mkdir","FS_mkdev","FS_symlink","FS_rename","FS_rmdir","FS_readdir","FS_readlink","FS_stat","FS_fstat","FS_lstat","FS_doChmod","FS_chmod","FS_lchmod","FS_fchmod","FS_doChown","FS_chown","FS_lchown","FS_fchown","FS_doTruncate","FS_truncate","FS_ftruncate","FS_utime","FS_open","FS_close","FS_isClosed","FS_llseek","FS_read","FS_write","FS_mmap","FS_msync","FS_ioctl","FS_writeFile","FS_cwd","FS_chdir","FS_createDefaultDirectories","FS_createDefaultDevices","FS_createSpecialDirectories","FS_createStandardStreams","FS_staticInit","FS_init","FS_quit","FS_findObject","FS_analyzePath","FS_createFile","FS_forceLoadFile","FS_absolutePath","FS_createFolder","FS_createLink","FS_joinPath","FS_mmapAlloc","FS_standardizePath","TTY","PIPEFS","SOCKFS","tempFixedLengthArray","miniTempWebGLFloatBuffers","miniTempWebGLIntBuffers","GL","AL","GLUT","EGL","GLEW","IDBStore","SDL","SDL_gfx","allocateUTF8","allocateUTF8OnStack","print","printErr","jstoi_s","InternalError","BindingError","throwInternalError","throwBindingError","registeredTypes","awaitingDependencies","typeDependencies","tupleRegistrations","structRegistrations","sharedRegisterType","whenDependentTypesAreResolved","getTypeName","getFunctionName","heap32VectorToArray","requireRegisteredType","usesDestructorStack","checkArgCount","getRequiredArgCount","createJsInvoker","UnboundTypeError","GenericWireTypeSize","EmValType","EmValOptionalType","throwUnboundTypeError","ensureOverloadTable","exposePublicSymbol","replacePublicSymbol","createNamedFunction","embindRepr","registeredInstances","getBasestPointer","getInheritedInstance","registeredPointers","registerType","integerReadValueFromPointer","enumReadValueFromPointer","floatReadValueFromPointer","assertIntegerRange","readPointer","runDestructors","craftInvokerFunction","embind__requireFunction","genericPointerToWireType","constNoSmartPtrRawPointerToWireType","nonConstNoSmartPtrRawPointerToWireType","init_RegisteredPointer","RegisteredPointer","RegisteredPointer_fromWireType","runDestructor","releaseClassHandle","finalizationRegistry","detachFinalizer_deps","detachFinalizer","attachFinalizer","makeClassHandle","init_ClassHandle","ClassHandle","throwInstanceAlreadyDeleted","deletionQueue","flushPendingDeletes","delayFunction","RegisteredClass","shallowCopyInternalPointer","downcastPointer","upcastPointer","validateThis","char_0","char_9","makeLegalFunctionName","emval_freelist","emval_handles","emval_symbols","getStringOrSymbol","Emval","emval_get_global","emval_returnValue","emval_lookupTypes","emval_methodCallers","emval_addMethodCaller"];Kp.forEach(ut),t.incrementExceptionRefcount=qp,t.decrementExceptionRefcount=Yp,t.getExceptionMessage=Rh;function Qp(){le("fetchSettings")}var Ph={638388:()=>{typeof t<"u"&&"mjDISABLESTRING mjENABLESTRING mjFRAMESTRING mjLABELSTRING mjRNDSTRING mjTIMERSTRING mjVISSTRING".split(" ").forEach(function(r){Object.defineProperty(t,r,{get:function(){return t["get_"+r]()},set:function(a){},enumerable:!0,configurable:!0})})}},Ih=Ke("___getTypeName"),Cl=Ke("_malloc"),em=Ke("___cxa_free_exception"),Rl=Ke("_fflush"),Xn=Ke("_free"),Pl=Ke("_emscripten_stack_get_end"),tm=Ke("_emscripten_stack_get_base"),Dh=Ke("_strerror"),Me=Ke("_setThrew"),Lh=Ke("__emscripten_tempret_set"),Fh=Ke("_emscripten_stack_init"),nm=Ke("_emscripten_stack_get_free"),Nh=Ke("__emscripten_stack_restore"),Uh=Ke("__emscripten_stack_alloc"),Oh=Ke("_emscripten_stack_get_current"),Il=Ke("___cxa_decrement_exception_refcount"),ua=Ke("___cxa_increment_exception_refcount"),Bh=Ke("___get_exception_message"),kh=Ke("___cxa_can_catch"),zh=Ke("___cxa_get_exception_ptr");function im(r){Ih=Te("__getTypeName",1),Cl=Te("malloc",1),em=Te("__cxa_free_exception",1),Rl=Te("fflush",1),Xn=Te("free",1),Pl=r.emscripten_stack_get_end,tm=r.emscripten_stack_get_base,Dh=Te("strerror",1),Me=Te("setThrew",2),Lh=Te("_emscripten_tempret_set",1),Fh=r.emscripten_stack_init,nm=r.emscripten_stack_get_free,Nh=r._emscripten_stack_restore,Uh=r._emscripten_stack_alloc,Oh=r.emscripten_stack_get_current,Il=Te("__cxa_decrement_exception_refcount",1),ua=Te("__cxa_increment_exception_refcount",1),Bh=Te("__get_exception_message",3),kh=Te("__cxa_can_catch",3),zh=Te("__cxa_get_exception_ptr",1)}var Vh={__assert_fail:Xs,__cxa_begin_catch:$s,__cxa_current_primary_exception:hr,__cxa_end_catch:js,__cxa_find_matching_catch_2:_l,__cxa_find_matching_catch_3:qs,__cxa_find_matching_catch_4:A,__cxa_rethrow:G,__cxa_rethrow_primary_exception:ie,__cxa_throw:K,__cxa_uncaught_exceptions:Q,__resumeException:Le,__syscall_dup3:wi,__syscall_fcntl64:Vd,__syscall_fstat64:Gd,__syscall_ioctl:Hd,__syscall_lstat64:Wd,__syscall_newfstatat:Xd,__syscall_openat:$d,__syscall_stat64:jd,_abort_js:qd,_embind_register_bigint:Zd,_embind_register_bool:Jd,_embind_register_class:gf,_embind_register_class_class_function:xf,_embind_register_class_constructor:Sf,_embind_register_class_function:bf,_embind_register_class_property:Mf,_embind_register_constant:Ef,_embind_register_emval:vh,_embind_register_enum:Tf,_embind_register_enum_value:Af,_embind_register_float:Rf,_embind_register_function:Pf,_embind_register_integer:If,_embind_register_memory_view:Df,_embind_register_optional:Ff,_embind_register_std_string:Nf,_embind_register_std_wstring:Gf,_embind_register_user_type:Hf,_embind_register_void:Wf,_emscripten_throw_longjmp:Xf,_emval_as:$f,_emval_call:jf,_emval_call_method:Yf,_emval_decref:El,_emval_get_global:Zf,_emval_get_method_caller:Qf,_emval_get_property:ep,_emval_incref:tp,_emval_is_number:np,_emval_is_string:ip,_emval_new_array:rp,_emval_new_cstring:sp,_emval_run_destructors:ap,_emval_take_value:op,_emval_throw:lp,_localtime_js:pp,_mktime_js:mp,_tzset_js:gp,clock_time_get:yp,emscripten_asm_const_int:bp,emscripten_date_now:Eh,emscripten_get_heap_max:Mp,emscripten_get_now:Mh,emscripten_resize_heap:Tp,environ_get:Cp,environ_sizes_get:Rp,exit:Dp,fd_close:Lp,fd_read:Np,fd_seek:Up,fd_write:Bp,invoke_ddd:Cg,invoke_dddi:$m,invoke_dddidi:jm,invoke_ddidi:Xm,invoke_di:qm,invoke_dii:Um,invoke_diii:_m,invoke_diiii:Wm,invoke_diiiidd:Gm,invoke_diiiidi:xm,invoke_diiiii:dm,invoke_diiiiii:Tm,invoke_diiiiiii:Ym,invoke_diiiiiiiii:Em,invoke_diiiiiiiiiiii:wm,invoke_fiii:kg,invoke_i:fm,invoke_id:Mg,invoke_ii:am,invoke_iid:rg,invoke_iidddd:Lg,invoke_iidiii:Fm,invoke_iidiiid:Dm,invoke_iif:Dg,invoke_iii:rm,invoke_iiid:Nm,invoke_iiididdddddd:Lm,invoke_iiidiiiiiiii:Im,invoke_iiii:cm,invoke_iiiidddiiiii:Jm,invoke_iiiii:gm,invoke_iiiiid:pg,invoke_iiiiii:cg,invoke_iiiiiii:ag,invoke_iiiiiiii:ig,invoke_iiiiiiiidd:mg,invoke_iiiiiiiii:Vm,invoke_iiiiiiiiii:og,invoke_iiiiiiiiiidddiiiiiiiii:Pm,invoke_iiiiiiiiiii:Bg,invoke_iiiiiiiiiiii:zg,invoke_iiiiiiiiiiiii:bg,invoke_iiij:lg,invoke_iiji:fg,invoke_j:Ug,invoke_ji:Sg,invoke_jiiii:hg,invoke_jij:xg,invoke_v:lm,invoke_vi:om,invoke_vid:sg,invoke_viddd:ug,invoke_vidddd:dg,invoke_vidi:Hm,invoke_vidiii:Cm,invoke_vii:um,invoke_viid:km,invoke_viiddi:yg,invoke_viiddidi:vg,invoke_viiddii:Zm,invoke_viidi:Bm,invoke_viidii:ym,invoke_viidiii:ng,invoke_viidiiid:eg,invoke_viidiiiii:Rm,invoke_viidiiiiiiii:Am,invoke_viii:sm,invoke_viiid:bm,invoke_viiidd:_g,invoke_viiidi:Om,invoke_viiididdddddd:tg,invoke_viiidiiiiiiii:Qm,invoke_viiii:mm,invoke_viiiiddd:gg,invoke_viiiidi:Rg,invoke_viiiifi:Pg,invoke_viiiii:hm,invoke_viiiiid:Sm,invoke_viiiiii:pm,invoke_viiiiiii:vm,invoke_viiiiiiii:zm,invoke_viiiiiiiiii:Tg,invoke_viiiiiiiiiidddiiiiiiiii:Km,invoke_viiiiiiiiiiid:Mm,invoke_viiiiiiiiiiiii:wg,invoke_viiiiiiiiiiiiiii:Vg,invoke_viiiiiiiiiiiiiiiiii:Ag,invoke_viiiij:Fg,invoke_viij:Ng,invoke_viijii:Og,invoke_vij:Ig,invoke_vijjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj:Eg,llvm_eh_typeid_for:kp},Yi=await Ne();function rm(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function sm(r,a,c,u){var p=Se();try{we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function am(r,a){var c=Se();try{return we(r)(a)}catch(u){if(ye(c),!(u instanceof V))throw u;Me(1,0)}}function om(r,a){var c=Se();try{we(r)(a)}catch(u){if(ye(c),!(u instanceof V))throw u;Me(1,0)}}function lm(r){var a=Se();try{we(r)()}catch(c){if(ye(a),!(c instanceof V))throw c;Me(1,0)}}function cm(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function hm(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function um(r,a,c){var u=Se();try{we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function dm(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function fm(r){var a=Se();try{return we(r)()}catch(c){if(ye(a),!(c instanceof V))throw c;Me(1,0)}}function pm(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function mm(r,a,c,u,p){var v=Se();try{we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function gm(r,a,c,u,p){var v=Se();try{return we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function _m(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function vm(r,a,c,u,p,v,E,C){var N=Se();try{we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function ym(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function xm(r,a,c,u,p,v,E){var C=Se();try{return we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Sm(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function bm(r,a,c,u,p){var v=Se();try{we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function Mm(r,a,c,u,p,v,E,C,N,$,ee,ue,pe){var ce=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe)}catch(ve){if(ye(ce),!(ve instanceof V))throw ve;Me(1,0)}}function Em(r,a,c,u,p,v,E,C,N,$){var ee=Se();try{return we(r)(a,c,u,p,v,E,C,N,$)}catch(ue){if(ye(ee),!(ue instanceof V))throw ue;Me(1,0)}}function wm(r,a,c,u,p,v,E,C,N,$,ee,ue,pe){var ce=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe)}catch(ve){if(ye(ce),!(ve instanceof V))throw ve;Me(1,0)}}function Tm(r,a,c,u,p,v,E){var C=Se();try{return we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Am(r,a,c,u,p,v,E,C,N,$,ee,ue){var pe=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue)}catch(ce){if(ye(pe),!(ce instanceof V))throw ce;Me(1,0)}}function Cm(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Rm(r,a,c,u,p,v,E,C,N){var $=Se();try{we(r)(a,c,u,p,v,E,C,N)}catch(ee){if(ye($),!(ee instanceof V))throw ee;Me(1,0)}}function Pm(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt){var gn=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt)}catch(Nt){if(ye(gn),!(Nt instanceof V))throw Nt;Me(1,0)}}function Im(r,a,c,u,p,v,E,C,N,$,ee,ue){var pe=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue)}catch(ce){if(ye(pe),!(ce instanceof V))throw ce;Me(1,0)}}function Dm(r,a,c,u,p,v,E){var C=Se();try{return we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Lm(r,a,c,u,p,v,E,C,N,$,ee,ue){var pe=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue)}catch(ce){if(ye(pe),!(ce instanceof V))throw ce;Me(1,0)}}function Fm(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Nm(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function Um(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function Om(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Bm(r,a,c,u,p){var v=Se();try{we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function km(r,a,c,u){var p=Se();try{we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function zm(r,a,c,u,p,v,E,C,N){var $=Se();try{we(r)(a,c,u,p,v,E,C,N)}catch(ee){if(ye($),!(ee instanceof V))throw ee;Me(1,0)}}function Vm(r,a,c,u,p,v,E,C,N){var $=Se();try{return we(r)(a,c,u,p,v,E,C,N)}catch(ee){if(ye($),!(ee instanceof V))throw ee;Me(1,0)}}function Gm(r,a,c,u,p,v,E){var C=Se();try{return we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Hm(r,a,c,u){var p=Se();try{we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function Wm(r,a,c,u,p){var v=Se();try{return we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function Xm(r,a,c,u,p){var v=Se();try{return we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function $m(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function jm(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function qm(r,a){var c=Se();try{return we(r)(a)}catch(u){if(ye(c),!(u instanceof V))throw u;Me(1,0)}}function Ym(r,a,c,u,p,v,E,C){var N=Se();try{return we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function Zm(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Jm(r,a,c,u,p,v,E,C,N,$,ee,ue){var pe=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue)}catch(ce){if(ye(pe),!(ce instanceof V))throw ce;Me(1,0)}}function Km(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt,gn){var Nt=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt,gn)}catch(Zi){if(ye(Nt),!(Zi instanceof V))throw Zi;Me(1,0)}}function Qm(r,a,c,u,p,v,E,C,N,$,ee,ue,pe){var ce=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe)}catch(ve){if(ye(ce),!(ve instanceof V))throw ve;Me(1,0)}}function eg(r,a,c,u,p,v,E,C){var N=Se();try{we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function tg(r,a,c,u,p,v,E,C,N,$,ee,ue,pe){var ce=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe)}catch(ve){if(ye(ce),!(ve instanceof V))throw ve;Me(1,0)}}function ng(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function ig(r,a,c,u,p,v,E,C){var N=Se();try{return we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function rg(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function sg(r,a,c){var u=Se();try{we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function ag(r,a,c,u,p,v,E){var C=Se();try{return we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function og(r,a,c,u,p,v,E,C,N,$){var ee=Se();try{return we(r)(a,c,u,p,v,E,C,N,$)}catch(ue){if(ye(ee),!(ue instanceof V))throw ue;Me(1,0)}}function lg(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function cg(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function hg(r,a,c,u,p){var v=Se();try{return we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;return Me(1,0),0n}}function ug(r,a,c,u,p){var v=Se();try{we(r)(a,c,u,p)}catch(E){if(ye(v),!(E instanceof V))throw E;Me(1,0)}}function dg(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function fg(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function pg(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function mg(r,a,c,u,p,v,E,C,N,$){var ee=Se();try{return we(r)(a,c,u,p,v,E,C,N,$)}catch(ue){if(ye(ee),!(ue instanceof V))throw ue;Me(1,0)}}function gg(r,a,c,u,p,v,E,C){var N=Se();try{we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function _g(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function vg(r,a,c,u,p,v,E,C){var N=Se();try{we(r)(a,c,u,p,v,E,C)}catch($){if(ye(N),!($ instanceof V))throw $;Me(1,0)}}function yg(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function xg(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;return Me(1,0),0n}}function Sg(r,a){var c=Se();try{return we(r)(a)}catch(u){if(ye(c),!(u instanceof V))throw u;return Me(1,0),0n}}function bg(r,a,c,u,p,v,E,C,N,$,ee,ue,pe){var ce=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe)}catch(ve){if(ye(ce),!(ve instanceof V))throw ve;Me(1,0)}}function Mg(r,a){var c=Se();try{return we(r)(a)}catch(u){if(ye(c),!(u instanceof V))throw u;Me(1,0)}}function Eg(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt,gn,Nt,Zi,Xg,$g,jg,qg,Yg,Zg,Jg,Kg,Qg,e_,t_,n_,i_,r_,s_,a_,o_,l_,c_,h_,u_,d_,f_,p_,m_,g_,__,v_,y_,x_,S_,b_,M_,E_,w_,T_,A_,C_,R_,P_,I_,D_,L_,F_,N_,U_,O_,B_,k_,z_,V_,G_,H_,W_,X_,$_,j_,q_,Y_,Z_,J_){var K_=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt,At,cn,Kt,gn,Nt,Zi,Xg,$g,jg,qg,Yg,Zg,Jg,Kg,Qg,e_,t_,n_,i_,r_,s_,a_,o_,l_,c_,h_,u_,d_,f_,p_,m_,g_,__,v_,y_,x_,S_,b_,M_,E_,w_,T_,A_,C_,R_,P_,I_,D_,L_,F_,N_,U_,O_,B_,k_,z_,V_,G_,H_,W_,X_,$_,j_,q_,Y_,Z_,J_)}catch(Hh){if(ye(K_),!(Hh instanceof V))throw Hh;Me(1,0)}}function wg(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce){var ve=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce)}catch(Qe){if(ye(ve),!(Qe instanceof V))throw Qe;Me(1,0)}}function Tg(r,a,c,u,p,v,E,C,N,$,ee){var ue=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee)}catch(pe){if(ye(ue),!(pe instanceof V))throw pe;Me(1,0)}}function Ag(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt){var At=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe,yt,ft,kt)}catch(cn){if(ye(At),!(cn instanceof V))throw cn;Me(1,0)}}function Cg(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function Rg(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Pg(r,a,c,u,p,v,E){var C=Se();try{we(r)(a,c,u,p,v,E)}catch(N){if(ye(C),!(N instanceof V))throw N;Me(1,0)}}function Ig(r,a,c){var u=Se();try{we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function Dg(r,a,c){var u=Se();try{return we(r)(a,c)}catch(p){if(ye(u),!(p instanceof V))throw p;Me(1,0)}}function Lg(r,a,c,u,p,v){var E=Se();try{return we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Fg(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Ng(r,a,c,u){var p=Se();try{we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function Ug(r){var a=Se();try{return we(r)()}catch(c){if(ye(a),!(c instanceof V))throw c;return Me(1,0),0n}}function Og(r,a,c,u,p,v){var E=Se();try{we(r)(a,c,u,p,v)}catch(C){if(ye(E),!(C instanceof V))throw C;Me(1,0)}}function Bg(r,a,c,u,p,v,E,C,N,$,ee){var ue=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee)}catch(pe){if(ye(ue),!(pe instanceof V))throw pe;Me(1,0)}}function kg(r,a,c,u){var p=Se();try{return we(r)(a,c,u)}catch(v){if(ye(p),!(v instanceof V))throw v;Me(1,0)}}function zg(r,a,c,u,p,v,E,C,N,$,ee,ue){var pe=Se();try{return we(r)(a,c,u,p,v,E,C,N,$,ee,ue)}catch(ce){if(ye(pe),!(ce instanceof V))throw ce;Me(1,0)}}function Vg(r,a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe){var yt=Se();try{we(r)(a,c,u,p,v,E,C,N,$,ee,ue,pe,ce,ve,Qe)}catch(ft){if(ye(yt),!(ft instanceof V))throw ft;Me(1,0)}}var Gh;function Gg(){Fh(),_e()}function Dl(){if(Ee>0){Ae=Dl;return}if(Gg(),Z(),Ee>0){Ae=Dl;return}function r(){k(!Gh),Gh=!0,t.calledRun=!0,!H&&(ne(),$t?.(t),t.onRuntimeInitialized?.(),mt("onRuntimeInitialized"),k(!t._main,'compiled without a main, but one is present. if you added it from JS, use Module["onRuntimeInitialized"]'),oe())}t.setStatus?(t.setStatus("Running..."),setTimeout(()=>{setTimeout(()=>t.setStatus(""),1),r()},1)):r(),ae()}function Hg(){var r=z,a=R,c=!1;z=R=u=>{c=!0};try{Rl(0),["stdout","stderr"].forEach(u=>{var p=M.analyzePath("/dev/"+u);if(p){var v=p.object,E=v.rdev,C=bt.ttys[E];C?.output?.length&&(c=!0)}})}catch{}z=r,R=a,c&&Vn("stdio streams had content in them that was not flushed. you should set EXIT_RUNTIME to 1 (see the Emscripten FAQ), or make sure to emit a newline when you printf etc.")}function Wg(){if(t.preInit)for(typeof t.preInit=="function"&&(t.preInit=[t.preInit]);t.preInit.length>0;)t.preInit.shift()();mt("preInit")}Wg(),Dl(),F?e=t:e=new Promise((r,a)=>{$t=r,dt=a});for(let r of Object.keys(t))r in i||Object.defineProperty(i,r,{configurable:!0,get(){xe(`Access to module property ('${r}') is no longer possible via the module constructor argument; Instead, use the result of the module constructor.`)}});return e}),Bd=Qb;var Xt=i=>document.getElementById(i),Ze={viewport:Xt("viewport"),loading:Xt("loading"),loadingText:Xt("loadingText"),errorPanel:Xt("errorPanel"),errorText:Xt("errorText"),retry:Xt("retryButton"),robotTitle:Xt("robotTitle"),pose:Xt("poseSelect"),play:Xt("playButton"),resetCamera:Xt("resetCameraButton"),selectedName:Xt("selectedName"),selectedDetail:Xt("selectedDetail"),selectionLabel:Xt("selectionLabel"),jointViz:Xt("jointVizToggle"),collision:Xt("collisionToggle"),transparent:Xt("transparentToggle"),labels:Xt("labelsToggle"),filter:Xt("filterInput"),list:Xt("structureList"),timeline:Xt("timeline"),frameText:Xt("frameText"),fpsText:Xt("fpsText"),warning:Xt("warningPanel")},kd;Ze.retry.addEventListener("click",()=>location.reload());function zd(i,e=""){console.error(i),Ze.loading.hidden=!0,Ze.errorPanel.hidden=!1;let t=i instanceof Error?i.message:String(i);Ze.errorText.textContent=`${e}${t}`}function nn(i){return typeof i=="object"&&i!==null&&"value"in i?i.value:i}function eM(){let i=new URLSearchParams(location.search),e=["manufacturer","robot_id","robot_variant"];for(let n of e)if(!i.get(n))throw new Error(`Viewer URL\u306B ${n} \u304C\u3042\u308A\u307E\u305B\u3093\u3002`);let t=new URLSearchParams;for(let n of["manufacturer","robot_id","robot_variant","capsule_id","run_id","stage","main_id","user_id"])i.get(n)&&t.set(n,i.get(n));return{api:t,source:i}}async function tM(i){let e=await fetch(i,{cache:"no-store"}),t=await e.json().catch(()=>({}));if(!e.ok)throw new Error(typeof t.detail=="string"?t.detail:`${e.status} ${e.statusText}`);return t}async function nM(i,e,t){let n=0;async function s(){for(;n<i.length;){let o=n++;await t(i[o],o)}}await Promise.all(Array.from({length:Math.min(e,i.length)},s))}function iM(i){if(i.byteLength<16)throw new Error("Motion data is empty or truncated.");let e=new DataView(i),t=new TextDecoder().decode(new Uint8Array(i,0,8));if(t!=="MEVAVW01"&&t!=="MEVAVW02")throw new Error("Unsupported motion data format.");let n=t==="MEVAVW02"?16:12,s=t==="MEVAVW02"?e.getUint32(8,!0):null,o=e.getUint32(t==="MEVAVW02"?12:8,!0);if(n+o>i.byteLength)throw new Error("Motion data header is truncated.");let l=JSON.parse(new TextDecoder().decode(new Uint8Array(i,n,o)));if(s!==null&&Number(l.format_version)!==s)throw new Error("Motion data version mismatch.");let h={},d=n+o;for(let f of l.blocks||[]){let g=d+Number(f.offset),y=g+Number(f.nbytes);if(g<d||y>i.byteLength)throw new Error(`Motion block is truncated: ${f.name}`);let m=i.slice(g,y);h[f.name]=f.dtype==="uint8"?new Uint8Array(m):f.dtype==="int32"?new Int32Array(m):new Float32Array(m)}return{header:l,arrays:h}}var nh=class{constructor(e,t,n){this.mujoco=e,this.config=t,this.sourceParams=n,this.model=null,this.data=null,this.mjvOption=null,this.mjvPerturb=null,this.mjvCamera=null,this.mjvScene=null,this.renderer=null,this.camera=null,this.controls=null,this.scene=new ms,this.geometryCache=new Map,this.renderObjects=[],this.bodyNames=[],this.jointNames=[],this.selected=null,this.activeTab="bodies",this.motion=null,this.motionJointAddresses=[],this.freeQposAddress=-1,this.motionFrame=0,this.playing=!1,this.playStartedAt=0,this.playStartedFrame=0,this.raf=null,this.renderQueued=!1,this.sceneDirty=!0,this.lastUiUpdate=0,this.warnings=new Set,this.raycaster=new Cs,this.pointer=new nt,this.bodyAxes=new Ps(.13),this.jointAxis=new Rs(new j(0,0,1),new j,.15,16043090,.035,.018),this.scene.add(this.bodyAxes,this.jointAxis),this.bodyAxes.visible=!1,this.jointAxis.visible=!1}async initialize(){await this.loadFilesAndModel(),this.createScene(),this.buildStructureUi(),this.bindUi(),await this.loadMotion(),this.applyRequestedPose(),this.resetCamera(),Ze.loading.hidden=!0,this.requestRender()}async loadFilesAndModel(){let e="/meva-robot",t=this.config.files.reduce((s,o)=>s+Number(o.size||0),0),n=0;this.mujoco.FS.mkdirTree(e),await nM(this.config.files,6,async s=>{let o=await fetch(s.url,{cache:"force-cache"});if(!o.ok)throw new Error(`Missing mesh / asset: ${s.path} (${o.status})`);let l=new Uint8Array(await o.arrayBuffer()),h=s.path.lastIndexOf("/");h>=0&&this.mujoco.FS.mkdirTree(`${e}/${s.path.slice(0,h)}`),this.mujoco.FS.writeFile(`${e}/${s.path}`,l),n+=l.byteLength,Ze.loadingText.textContent=`Robot assets ${Math.min(100,Math.round(n/Math.max(1,t)*100))}%`}),Ze.loadingText.textContent="MuJoCo model\u3092\u30B3\u30F3\u30D1\u30A4\u30EB\u3057\u3066\u3044\u307E\u3059\u2026";try{this.model=this.mujoco.MjModel.from_xml_path(`${e}/${this.config.model_path}`)}catch(s){throw new Error(`XML load error: ${s instanceof Error?s.message:s}`)}if(!this.model)throw new Error("XML load error: MuJoCo did not create a model.");this.data=new this.mujoco.MjData(this.model),this.mjvOption=new this.mujoco.MjvOption,this.mjvPerturb=new this.mujoco.MjvPerturb,this.mjvCamera=new this.mujoco.MjvCamera,this.mjvScene=new this.mujoco.MjvScene(this.model,Math.max(4096,Number(this.model.ngeom||0)*8)),this.mujoco.mj_forward(this.model,this.data),this.bodyNames=Array.from({length:Number(this.model.nbody)},(s,o)=>this.nameOf(this.mujoco.mjtObj.mjOBJ_BODY,o,`body_${o}`)),this.jointNames=Array.from({length:Number(this.model.njnt)},(s,o)=>this.nameOf(this.mujoco.mjtObj.mjOBJ_JOINT,o,`joint_${o}`))}nameOf(e,t,n){try{return this.mujoco.mj_id2name(this.model,nn(e),t)||n}catch{return n}}createScene(){let e;try{let n=document.createElement("canvas");if(e=n.getContext("webgl2")||n.getContext("webgl"),!e)throw new Error("WebGL unavailable. Chrome / Edge\u306EGPU\u8A2D\u5B9A\u3092\u78BA\u8A8D\u3057\u3066\u304F\u3060\u3055\u3044\u3002");this.renderer=new ul({antialias:!0,powerPreference:"high-performance"})}catch(n){throw new Error(`WebGL initialization failure: ${n instanceof Error?n.message:n}`)}this.renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5)),this.renderer.outputColorSpace=dn,this.renderer.domElement.tabIndex=0,Ze.viewport.prepend(this.renderer.domElement),this.scene.background=new ht(1053978),this.camera=new fn(42,1,.01,200),this.camera.up.set(0,0,1),this.controls=new ml(this.camera,this.renderer.domElement),this.controls.enableDamping=!1,this.controls.screenSpacePanning=!0,this.controls.addEventListener("change",()=>this.requestRender(!1)),this.scene.add(new ws(15266039,2239282,2.2));let t=new As(16777215,2.5);t.position.set(-2,-3,5),this.scene.add(t),this.resize(),this.resizeObserver=new ResizeObserver(()=>{this.resize(),this.requestRender(!1)}),this.resizeObserver.observe(Ze.viewport),this.renderer.domElement.addEventListener("pointerdown",n=>this.pointerDown={x:n.clientX,y:n.clientY}),this.renderer.domElement.addEventListener("pointerup",n=>{this.pointerDown&&Math.hypot(n.clientX-this.pointerDown.x,n.clientY-this.pointerDown.y)<4&&this.pick(n),this.pointerDown=null})}resize(){let e=Ze.viewport.getBoundingClientRect();!this.renderer||e.width<1||e.height<1||(this.renderer.setSize(e.width,e.height,!1),this.camera.aspect=e.width/e.height,this.camera.updateProjectionMatrix())}buildStructureUi(){document.querySelectorAll(".tabs button").forEach(e=>e.addEventListener("click",()=>{document.querySelectorAll(".tabs button").forEach(t=>t.classList.toggle("active",t===e)),this.activeTab=e.dataset.tab,this.refreshList()})),Ze.filter.addEventListener("input",()=>this.refreshList()),this.refreshList()}refreshList(){let e=this.activeTab==="bodies"?"body":"joint",t=e==="body"?this.bodyNames:this.jointNames,n=Ze.filter.value.trim().toLowerCase(),s=document.createDocumentFragment();t.forEach((o,l)=>{if(n&&!o.toLowerCase().includes(n))return;let h=document.createElement("button");h.type="button",h.className=`structure-row${this.selected?.type===e&&this.selected.id===l?" selected":""}`,h.textContent=o;let d=document.createElement("small");d.textContent=`#${l}`,h.appendChild(d),h.addEventListener("click",()=>this.select(e,l)),s.appendChild(h)}),Ze.list.replaceChildren(s)}bindUi(){Ze.resetCamera.addEventListener("click",()=>this.resetCamera()),Ze.pose.addEventListener("change",()=>this.applyPose(Ze.pose.value)),Ze.play.addEventListener("click",()=>this.setPlaying(!this.playing)),Ze.timeline.addEventListener("input",()=>{this.setPlaying(!1),this.applyMotionFrame(Number(Ze.timeline.value))}),Ze.jointViz.addEventListener("change",()=>{this.sceneDirty=!0,this.requestRender()}),Ze.collision.addEventListener("change",()=>{this.sceneDirty=!0,this.requestRender()}),Ze.transparent.addEventListener("change",()=>this.updateAppearance()),Ze.labels.addEventListener("change",()=>{this.updateSelectionHelpers(),this.requestRender(!1)}),window.addEventListener("keydown",e=>{e.code==="Space"&&e.target?.tagName!=="INPUT"&&(e.preventDefault(),this.setPlaying(!this.playing)),e.key.toLowerCase()==="r"&&this.resetCamera()}),window.addEventListener("pagehide",()=>this.dispose(),{once:!0})}async loadMotion(){let e=Ze.pose.querySelector('option[value="motion"]');if(!this.config.motion_url){e.disabled=!0;return}try{let t=await fetch(this.config.motion_url,{cache:"no-store"});if(!t.ok){let n=await t.json().catch(()=>({}));throw new Error(n.detail||`${t.status} ${t.statusText}`)}if(this.motion=iM(await t.arrayBuffer()),this.motion.header.kind!=="retarget")throw new Error("Selected data is not Robot motion.");this.prepareMotionMapping(),Ze.timeline.max=Math.max(0,Number(this.motion.header.frame_count)-1),Ze.timeline.disabled=!1,Ze.play.disabled=!1,Ze.fpsText.textContent=`${this.motionFps().toFixed(2)} FPS`}catch(t){e.disabled=!0,this.warn(`Motion load error: ${t instanceof Error?t.message:t}`)}}motionFps(){let e=Number(this.motion?.header?.fps);return Number.isFinite(e)&&e>0?e:30}prepareMotionMapping(){let e=nn(this.mujoco.mjtJoint.mjJNT_FREE);this.freeQposAddress=-1;for(let t=0;t<Number(this.model.njnt);t++)if(Number(this.model.jnt_type[t])===e){this.freeQposAddress=Number(this.model.jnt_qposadr[t]);break}this.motionJointAddresses=(this.motion.header.joint_names||[]).map(t=>{let n=this.mujoco.mj_name2id(this.model,nn(this.mujoco.mjtObj.mjOBJ_JOINT),t);return n>=0?Number(this.model.jnt_qposadr[n]):-1})}applyRequestedPose(){let e=this.sourceParams.get("pose"),t=Number(this.sourceParams.get("frame"));e==="standing"?Ze.pose.value="standing":e==="motion"&&this.motion?Ze.pose.value="motion":Ze.pose.value="model_default",this.applyPose(Ze.pose.value,Number.isFinite(t)?t:0)}applyPose(e,t=0){if(this.setPlaying(!1),e==="motion"){if(!this.motion){this.warn("Motion data is unavailable."),Ze.pose.value="model_default";return}this.applyMotionFrame(t);return}if(e==="standing"){this.applyPoseDefinition(this.config.standing_pose,"Standing Pose")||(this.warn("Standing Pose\u306F\u3053\u306ERobot manifest\u306B\u5B9A\u7FA9\u3055\u308C\u3066\u3044\u307E\u305B\u3093\u3002"),Ze.pose.value="model_default",this.applyPose("model_default"));return}this.mujoco.mj_resetData(this.model,this.data),this.mujoco.mj_forward(this.model,this.data),this.motionFrame=0,this.sceneDirty=!0,this.updateMotionUi(),this.requestRender()}applyPoseDefinition(e,t){if(!e||typeof e!="object")return!1;let n=e.type||(Array.isArray(e.qpos)?"qpos":"");try{if(n==="model_default")this.mujoco.mj_resetData(this.model,this.data);else if(n==="keyframe"){let s=this.mujoco.mj_name2id(this.model,nn(this.mujoco.mjtObj.mjOBJ_KEY),String(e.name||""));if(s<0)throw new Error(`keyframe '${e.name||""}' not found`);this.mujoco.mj_resetDataKeyframe(this.model,this.data,s)}else if(n==="qpos"){if(!Array.isArray(e.qpos)||e.qpos.length!==Number(this.model.nq))throw new Error(`invalid qpos length (expected ${this.model.nq})`);if(!e.qpos.every(Number.isFinite))throw new Error("qpos contains a non-finite value");this.mujoco.mj_resetData(this.model,this.data),this.data.qpos.set(e.qpos)}else throw new Error(`unsupported pose type '${n}'`);return this.mujoco.mj_forward(this.model,this.data),this.sceneDirty=!0,this.requestRender(),!0}catch(s){return this.warn(`${t} load failure: ${s instanceof Error?s.message:s}`),!1}}applyMotionFrame(e){if(!this.motion)return;let t=Number(this.motion.header.frame_count),n=Math.max(0,Math.min(t-1,Math.round(e))),s=this.motion.arrays,o=s.root_pos,l=s.root_rot,h=s.dof_pos,d=this.motion.header.joint_names||[],f=this.data.qpos;if(f.set(this.model.qpos0),this.freeQposAddress>=0){let y=this.freeQposAddress;if(!o||!l){this.warn("Invalid qpos: motion root pose is missing.");return}if(f[y]=o[n*3],f[y+1]=o[n*3+1],f[y+2]=o[n*3+2],String(this.motion.header.root_rot_order||"wxyz").toLowerCase()==="xyzw")f[y+3]=l[n*4+3],f[y+4]=l[n*4],f[y+5]=l[n*4+1],f[y+6]=l[n*4+2];else for(let S=0;S<4;S++)f[y+3+S]=l[n*4+S]}if(!h||h.length<t*d.length){this.warn("Invalid qpos: motion joint data is missing.");return}for(let y=0;y<d.length;y++)this.motionJointAddresses[y]>=0&&(f[this.motionJointAddresses[y]]=h[n*d.length+y]);for(let y=0;y<f.length;y++)if(!Number.isFinite(f[y])){this.warn(`Invalid qpos at index ${y}.`);return}this.mujoco.mj_forward(this.model,this.data),this.motionFrame=n,this.sceneDirty=!0;let g=performance.now();(!this.playing||g-this.lastUiUpdate>=100)&&(this.lastUiUpdate=g,this.updateMotionUi()),this.requestRender()}setPlaying(e){(!this.motion||Ze.pose.value!=="motion")&&(e=!1),this.playing=!!e,Ze.play.textContent=this.playing?"PAUSE":"PLAY",this.playing&&(this.playStartedAt=performance.now(),this.playStartedFrame=this.motionFrame,this.requestRender())}updateMotionUi(){Ze.timeline.value=String(this.motionFrame),Ze.frameText.textContent=this.motion?`FRAME ${this.motionFrame+1} / ${this.motion.header.frame_count}`:"FRAME \u2014"}requestRender(e=!0){e&&(this.sceneDirty=!0),this.raf===null&&(this.raf=requestAnimationFrame(t=>{try{this.tick(t)}catch(n){this.setPlaying(!1),zd(n,"Rendering error: ")}}))}tick(e){if(this.raf=null,this.playing){let t=Number(this.motion.header.frame_count),n=Math.floor((e-this.playStartedAt)*this.motionFps()/1e3),s=(this.playStartedFrame+n)%t;s!==this.motionFrame&&this.applyMotionFrame(s)}this.sceneDirty&&this.updateMuJoCoScene(),this.updateSelectionHelpers(),this.renderer.render(this.scene,this.camera),this.playing&&this.requestRender(!1)}geometryFor(e){let t=Number(e.type),n=Number(e.dataid),s=Number(e.objid);t===nn(this.mujoco.mjtGeom.mjGEOM_MESH)&&Number(e.objtype)===nn(this.mujoco.mjtObj.mjOBJ_GEOM)&&s>=0&&s<Number(this.model.ngeom)&&(n=Number(this.model.geom_dataid[s]));let o=Array.from(e.size||[]),l=`${t}:${n}:${o.map(f=>Number(f).toPrecision(7)).join(",")}`;if(this.geometryCache.has(l))return{key:l,geometry:this.geometryCache.get(l)};let h=this.mujoco.mjtGeom,d;return t===nn(h.mjGEOM_PLANE)?d=new sr(Math.min(20,2*(o[0]||10)),Math.min(20,2*(o[1]||10))):t===nn(h.mjGEOM_SPHERE)?d=new zr(o[0],24,16):t===nn(h.mjGEOM_CAPSULE)?(d=new Ss(o[0],2*o[2],8,16),d.rotateX(Math.PI/2)):t===nn(h.mjGEOM_BOX)?d=new Fi(2*o[0],2*o[1],2*o[2]):t===nn(h.mjGEOM_CYLINDER)?(d=new rr(o[0],o[0],2*o[2],24),d.rotateX(Math.PI/2)):t===nn(h.mjGEOM_ELLIPSOID)?(d=new zr(1,24,16),d.scale(o[0],o[1],o[2])):t===nn(h.mjGEOM_MESH)?d=this.meshGeometry(n):[h.mjGEOM_ARROW,h.mjGEOM_ARROW1,h.mjGEOM_ARROW2,h.mjGEOM_LINE].some(f=>t===nn(f))?(d=new rr(Math.max(.001,o[0]),Math.max(.001,o[0]),Math.max(.001,2*o[2]),10),d.rotateX(Math.PI/2)):(d=new Yt,this.warn(`Unsupported MuJoCo geometry type ${t} is hidden.`)),this.geometryCache.set(l,d),{key:l,geometry:d}}meshGeometry(e){if(e<0||e>=Number(this.model.nmesh))return this.warn(`MuJoCo decoration mesh ${e} is outside the model mesh table and was hidden.`),new Yt;let t=Number(this.model.mesh_vertadr[e]),n=Number(this.model.mesh_vertnum[e]),s=Number(this.model.mesh_faceadr[e]),o=Number(this.model.mesh_facenum[e]);if(!n||!o)throw new Error(`Unsupported asset: mesh ${e} has no triangles`);let l=new Float32Array(n*3);for(let f=0;f<l.length;f++)l[f]=this.model.mesh_vert[t*3+f];let h=new Uint32Array(o*3);for(let f=0;f<h.length;f++)h[f]=this.model.mesh_face[s*3+f];let d=new Yt;return d.setAttribute("position",new vn(l,3)),d.setIndex(new vn(h,1)),d.computeVertexNormals(),d.computeBoundingSphere(),d}updateMuJoCoScene(){let e=nn(this.mujoco.mjtVisFlag.mjVIS_JOINT);this.mjvOption.flags[e]=Ze.jointViz.checked?1:0,this.mjvOption.geomgroup?.length>3&&(this.mjvOption.geomgroup[3]=Ze.collision.checked?1:0),this.mujoco.mjv_updateScene(this.model,this.data,this.mjvOption,this.mjvPerturb,this.mjvCamera,nn(this.mujoco.mjtCatBit.mjCAT_ALL),this.mjvScene);let t=this.mjvScene.geoms,n=0,s=!1;try{n=t.size();for(let o=0;o<n;o++){let l=t.get(o);if(l)try{let h=this.geometryFor(l),d=this.renderObjects[o];d?d.userData.geometryKey!==h.key&&(d.geometry=h.geometry):(d=new yn(h.geometry,new bs({side:li})),d.matrixAutoUpdate=!1,this.renderObjects[o]=d,this.scene.add(d)),d.userData.geometryKey=h.key,d.userData.objtype=Number(l.objtype),d.userData.objid=Number(l.objid),d.visible=h.geometry.getAttribute("position")!==void 0,d.matrix.set(l.mat[0],l.mat[1],l.mat[2],l.pos[0],l.mat[3],l.mat[4],l.mat[5],l.pos[1],l.mat[6],l.mat[7],l.mat[8],l.pos[2],0,0,0,1),d.matrixWorldNeedsUpdate=!0;let f=d.material,g=`${l.rgba[0]},${l.rgba[1]},${l.rgba[2]},${l.rgba[3]},${l.shininess}`;f.userData.rgbaKey!==g&&(f.userData.rgbaKey=g,f.color.setRGB(l.rgba[0],l.rgba[1],l.rgba[2],dn),f.userData.baseOpacity=Number(l.rgba[3]),f.shininess=Math.max(8,Number(l.shininess||0)*128),s=!0)}finally{l.delete()}}}finally{t.delete()}for(let o=n;o<this.renderObjects.length;o++)this.renderObjects[o].visible=!1;this.sceneDirty=!1,s&&this.updateAppearance(!1)}updateAppearance(e=!0){let t=Ze.transparent.checked?.34:1;for(let n of this.renderObjects){if(!n)continue;let s=(n.material.userData.baseOpacity??1)*t;n.material.opacity=s,n.material.transparent=s<.999,n.material.depthWrite=s>=.999,n.material.needsUpdate=!0}e&&this.requestRender(!1)}pick(e){let t=this.renderer.domElement.getBoundingClientRect();this.pointer.set((e.clientX-t.left)/t.width*2-1,-(e.clientY-t.top)/t.height*2+1),this.raycaster.setFromCamera(this.pointer,this.camera);let n=this.raycaster.intersectObjects(this.renderObjects.filter(l=>l?.visible),!1)[0];if(!n)return;let s=n.object.userData.objtype,o=n.object.userData.objid;if(s===nn(this.mujoco.mjtObj.mjOBJ_GEOM)&&o>=0){let l=Number(this.model.geom_bodyid[o]);this.select("body",l)}else s===nn(this.mujoco.mjtObj.mjOBJ_JOINT)&&o>=0&&this.select("joint",o)}select(e,t){this.selected={type:e,id:t};let n=e==="body"?this.bodyNames[t]:this.jointNames[t];if(Ze.selectedName.textContent=n||`${e}_${t}`,e==="joint"){let s=Number(this.model.jnt_type[t]),o=Number(this.model.jnt_bodyid[t]);Ze.selectedDetail.textContent=`Joint #${t} \xB7 Body: ${this.bodyNames[o]} \xB7 Type: ${this.jointTypeName(s)}`}else{let s=Number(this.model.body_parentid[t]);Ze.selectedDetail.textContent=`Body / Link #${t} \xB7 Parent: ${this.bodyNames[s]||"world"}`}this.refreshList(),this.updateSelectionHelpers(),this.requestRender(!1)}jointTypeName(e){let t=this.mujoco.mjtJoint;for(let[n,s]of Object.entries(t))if(nn(s)===e)return n.replace("mjJNT_","");return String(e)}updateSelectionHelpers(){if(this.bodyAxes.visible=!1,this.jointAxis.visible=!1,Ze.selectionLabel.hidden=!0,!this.selected)return;let e;if(this.selected.type==="body"){let t=this.selected.id;e=new j(this.data.xpos[t*3],this.data.xpos[t*3+1],this.data.xpos[t*3+2]),this.bodyAxes.position.copy(e);let n=this.data.xmat,s=new Ot().set(n[t*9],n[t*9+1],n[t*9+2],0,n[t*9+3],n[t*9+4],n[t*9+5],0,n[t*9+6],n[t*9+7],n[t*9+8],0,0,0,0,1);this.bodyAxes.quaternion.setFromRotationMatrix(s),this.bodyAxes.visible=!0}else{let t=this.selected.id;e=new j(this.data.xanchor[t*3],this.data.xanchor[t*3+1],this.data.xanchor[t*3+2]);let n=new j(this.data.xaxis[t*3],this.data.xaxis[t*3+1],this.data.xaxis[t*3+2]).normalize();this.jointAxis.position.copy(e),this.jointAxis.setDirection(n),this.jointAxis.visible=Ze.jointViz.checked}if(Ze.labels.checked&&e){let t=e.clone().project(this.camera),n=this.renderer.domElement.getBoundingClientRect();t.z>=-1&&t.z<=1&&(Ze.selectionLabel.textContent=this.selected.type==="body"?this.bodyNames[this.selected.id]:this.jointNames[this.selected.id],Ze.selectionLabel.style.left=`${(t.x*.5+.5)*n.width+8}px`,Ze.selectionLabel.style.top=`${(-t.y*.5+.5)*n.height-12}px`,Ze.selectionLabel.hidden=!1)}}resetCamera(){if(!this.model||!this.camera)return;let e=[];for(let o=1;o<Number(this.model.nbody);o++)e.push(new j(this.data.xpos[o*3],this.data.xpos[o*3+1],this.data.xpos[o*3+2]));let t=new oi().setFromPoints(e),n=t.getCenter(new j),s=Math.max(.5,t.getSize(new j).length());this.controls.target.copy(n),this.camera.position.set(n.x+s*1.25,n.y-s*1.8,n.z+s*.65),this.camera.near=Math.max(.005,s/1e3),this.camera.far=Math.max(50,s*30),this.camera.updateProjectionMatrix(),this.controls.update(),this.requestRender(!1)}warn(e){this.warnings.add(e),Ze.warning.hidden=!1,Ze.warning.textContent=[...this.warnings].join(`
`)}dispose(){this.raf!==null&&cancelAnimationFrame(this.raf),this.resizeObserver?.disconnect(),this.controls?.dispose();for(let e of this.renderObjects)e?.material?.dispose();for(let e of this.geometryCache.values())e.dispose();this.renderer?.dispose();for(let e of[this.mjvScene,this.mjvCamera,this.mjvPerturb,this.mjvOption,this.data,this.model])e?.delete()}};async function rM(){try{let{api:i,source:e}=eM();Ze.loadingText.textContent="Robot configuration\u3092\u53D6\u5F97\u3057\u3066\u3044\u307E\u3059\u2026";let t=await tM(`/api/retarget/robots/viewer/browser/config?${i}`);Ze.robotTitle.textContent=`${t.robot.robot_name} / ${t.robot.variant_name}`,document.title=`${t.robot.variant_name} \u2014 Robot Viewer`,t.standing_pose||(Ze.pose.querySelector('option[value="standing"]').textContent="STANDING POSE (UNDEFINED)"),Ze.loadingText.textContent="MuJoCo WASM \u3092\u521D\u671F\u5316\u3057\u3066\u3044\u307E\u3059\u2026";let n;try{n=await Bd({locateFile:s=>s.endsWith(".wasm")?"/assets/robot-viewer/mujoco.wasm":s})}catch(s){throw new Error(`MuJoCo WASM initialization failure: ${s instanceof Error?s.message:s}`)}kd=new nh(n,t,e),await kd.initialize()}catch(i){zd(i)}}rM();
/*! Bundled license information:

three/build/three.core.js:
three/build/three.module.js:
  (**
   * @license
   * Copyright 2010-2026 Three.js Authors
   * SPDX-License-Identifier: MIT
   *)
*/
