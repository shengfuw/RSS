
*====Data Preprocess=====================================================================*
cd "/Users/shengfu/Desktop/臺大/高等量化方法 郭貞蘭/期末報告"
set more off

**Students
//87-103
use "students(87-109)_raw.dta", clear

replace scode = 學校代碼 if scode == ""
lab var scode "學校代碼"

replace sname = 學校名稱 if sname == ""
lab var sname "學校名稱"

split(日間∕進修別)
replace dn = 日間∕進修別1 if dn == ""
lab var dn "日間／進修別代碼"
rename dn dncode
replace dn1 = 日間∕進修別2 if dn1 == ""
lab var dn1 "日間／進修別"
rename dn1 dn

split(日夜別)
replace dncode = 日夜別1 if dn == ""
replace dn = 日夜別2 if dn == ""

split(等級別)
replace level = 等級別1 if level == ""
lab var level "等級別代碼"
rename level levelcode
replace level1 = 等級別2 if level1 == ""
lab var level1 "等級別"
rename level1 level

replace bcode = 科系代碼 if bcode == ""
lab var bcode "科系代碼"

replace bname = 科系名稱 if bname == ""
lab var bname "科系名稱"

replace student = 總計 if student == "" 
gen student_n = real(student)
replace student_n = . if 總計 == "-"
lab var student_n "學生總數"

replace male = 男生計 if male == "" 
gen male_n = real(male)
replace male_n = . if 男生計 == "-"
lab var male_n "學生男生計"

replace female = 女生計 if female == "" 
gen female_n = real(female)
replace female_n = . if 女生計 == "-"
lab var female_n "學生女生計"

replace m1 = 一年級男生 if m1 == ""
gen m1_n = real(m1)
replace m1_n = . if 一年級男生 == "-"
lab var m1_n "一年級男生"

replace f1 = 一年級女生 if f1 == "" 
gen f1_n = real(f1)
replace f1_n = . if 一年級女生 == "-"
lab var f1_n "一年級女生"

replace m2 = 二年級男生 if m2 == "" 
gen m2_n = real(m2)
replace m2_n = . if 二年級男生 == "-"
lab var m2_n "二年級男生"

replace f2 = 二年級女生 if f2 == ""
gen f2_n = real(f2) 
replace f2_n = . if 二年級女生 == "-"
lab var f2_n "二年級女生"

replace m3 = 三年級男生 if m3 == ""
gen m3_n = real(m3) 
replace m3_n = . if 三年級男生 == "-"
lab var m3_n "三年級男生"

replace f3 = 三年級女生 if f3 == ""
gen f3_n = real(f3) 
replace f3_n = . if 三年級女生 == "-"
lab var f3_n "三年級女生"

replace m4 = 四年級男生 if m4 == "" 
gen m4_n = real(m4)
replace m4_n = . if 四年級男生 == "-"
lab var m4_n "四年級男生"

replace f4 = 四年級女生 if f4 == "" 
gen f4_n = real(f4)
replace f4_n = . if 四年級女生 == "-"
lab var f4_n "四年級女生"

replace m5 = 五年級男生 if m5 == "" 
gen m5_n = real(m5)
replace m5_n = . if 五年級男生 == "-"
lab var m5_n "五年級男生"

replace f5 = 五年級女生 if f5 == "" 
gen f5_n = real(f5)
replace f5_n = . if 五年級女生 == "-"
lab var f5_n "五年級女生"

replace m6 = 六年級男生 if m6 == "" 
gen m6_n = real(m6)
replace m6_n = . if 六年級男生 == "-"
lab var m6_n "六年級男生"

replace f6 = 六年級女生 if f6 == ""
gen f6_n = real(f6) 
replace f6_n = . if 六年級女生 == "-"
lab var f6_n "六年級女生"

replace m7 = 七年級男生 if m7 == "" 
gen m7_n = real(m7)
replace m7_n = . if 七年級男生 == "-"
lab var m7_n "七年級男生"

replace f7 = 七年級女生 if f7 == ""
gen f7_n = real(f7) 
replace f7_n = . if 七年級女生 == "-"
lab var f7_n "七年級女生"

replace m8 = 延修生男生 if m8 == "" 
gen m8_n = real(m8)
replace m8_n = . if 延修生男生 == "-"
lab var m8_n "延修生男生"

replace f8 = 延修生女生 if f8 == "" 
gen f8_n = real(f8)
replace f8_n = . if 延修生女生 == "-"
lab var f8_n "延修生女生"

split(縣市名稱)
replace ctycode = 縣市名稱1 if ctycode == ""
lab var ctycode "縣市代碼"
rename ctycode citycode
replace ctyzone_name = 縣市名稱2 if ctyzone_name == ""
lab var ctyzone_name "縣市名稱"
rename ctyzone_name city

split(體系別)
split(way)
replace way1 = 體系別1 if way1 == ""
replace way2 = 體系別2 if way2 == ""
lab var way1 "體系別代碼"
renam way1 waycode
lab var way2 "體系別" 
drop way
renam way2 way

drop if scode == "學校代碼" | scode == "學校" | scode == "代碼" | scode == ""

order year sy ey scode sname bcode bname levelcode level dncode dn citycode city waycode way *_n
drop 學校代碼-體系別2 
sort scode bname levelcode year

save "students(87-109).dta", replace

//61-86
use "students(61-90)_raw.dta", clear
gen year = real(學年度)
gen sy = year + 1911
gen ey = year + 1912
rename 學校代碼 scode
rename 學校名稱 sname
rename 日夜別 dncode
rename 等級別 levelcode
rename 科系代碼 bcode 
rename 科系名稱 bname
gen student_n = real(學生數)
gen male_n = real(男生)
gen female_n = real(女生)
gen m1_n = real(一男)
gen f1_n = real(一女)
gen m2_n = real(二男)
gen f2_n = real(二女)
gen m3_n = real(三男)
gen f3_n = real(三女)
gen m4_n = real(四男)
gen f4_n = real(四女)
gen m5_n = real(五男)
gen f5_n = real(五女)
gen m6_n = real(六男)
gen f6_n = real(六女)
gen m7_n = real(七男)
gen f7_n = real(七女)
gen m8_n = real(延修男)
gen f8_n = real(延修女)
gen dn = d1
replace dn = d3 if dn == ""
replace dn = d5 if dn == ""
replace dn = d7 if dn == ""
gen level = d2 if level == ""
replace level = d4 if level == ""
replace level = d6 if level == ""
replace level = d8 if level == ""

replace dn = dncode if dncode != "D" & dncode != "F" & dncode != "N" & dncode != "N" & dncode != "P" & dncode != "S" & dn == ""
replace dncode = "N" if dncode == "夜"
replace dncode = "D" if dncode == "日"
replace dncode = "S" if dncode == "暑" | dncode == "暑期"
replace dncode = "F" if dncode == "第二部"
replace dncode = "P" if dncode == "進修" | dncode == "進修班"

replace level = levelcode if levelcode != "2" & levelcode != "3" & levelcode != "5" & levelcode != "B" & levelcode != "C" & levelcode != "D" & levelcode != "M" & level == ""
replace levelcode = "3" if levelcode == "三專"
replace levelcode = "2" if levelcode == "二專"
replace levelcode = "5" if levelcode == "五專"
replace levelcode = "D" if levelcode == "博士"
replace levelcode = "B" if levelcode == "大學" | levelcode == "學士"
replace levelcode = "M" if levelcode == "碩士"

order year sy ey scode sname bcode bname levelcode level dncode dn *_n
drop 學年度-d8
 
keep if year <= 86 
 
save "students(61-86).dta", replace 

//Append
use "students(87-109).dta", clear
append using "students(61-86).dta" 
replace bname = subinstr(bname, "　　　　　", "", .)
replace bname = subinstr(bname, "　", "", .)

//分析對象：日間部學士
keep if dncode == "D"
keep if levelcode == "B"

rename male_n s_male_n 
rename female_n s_female_n 
rename m* s_m*
rename f* s_f*

egen y_sc_bc_bn = concat(year scode bcode bname), punct("-")
egen y_sc_bc = concat(year scode bcode), punct("-")
egen y_sc_bn = concat(year scode bname), punct("-")

// 同一年中，同校裡有相同科系代碼（可能是分組）-> 加總人數
duplicates tag y_sc_bc, gen(stag)
bysort y_sc_bc: gen spickone = (_n == 1)
local vars = "student_n s_male_n s_female_n s_m1_n s_f1_n s_m2_n s_f2_n s_m3_n s_f3_n s_m4_n s_f4_n s_m5_n s_f5_n s_m6_n s_f6_n s_m7_n s_f7_n s_m8_n s_f8_n"
foreach v in `vars' {
	bysort y_sc_bc: egen `v'_temp = total(`v') 
	quietly replace `v' = `v'_temp if stag & spickone
}
keep if spickone
drop *_temp spickone 

// 同一年中，同校裡有相同科系名稱 -> 加總人數
duplicates tag y_sc_bn, gen(stag2)
bysort y_sc_bn: gen spickone2 = (_n == 1)
local vars = "student_n s_male_n s_female_n s_m1_n s_f1_n s_m2_n s_f2_n s_m3_n s_f3_n s_m4_n s_f4_n s_m5_n s_f5_n s_m6_n s_f6_n s_m7_n s_f7_n s_m8_n s_f8_n"
foreach v in `vars' {
	bysort y_sc_bn: egen `v'_temp = total(`v') 
	quietly replace `v' = `v'_temp if stag2 & spickone2
}
keep if spickone2
drop *_temp spickone2

sort scode bname levelcode year
save "students.dta", replace

**Teachers
//87-109
use "teachers(87-109)_raw.dta", clear
gen t_all_n = real(t_all)
gen t_all_male_n = real(t_all_male)
gen t_all_female_n = real(t_all_female)
gen t_professor_male_n = real(t_professor_male)
gen t_professor_female_n = real(t_professor_female)
gen t_associate_male_n = real(t_associate_male)
gen t_associate_female_n = real(t_associate_female)
gen t_assistant_male_n = real(t_assistant_male)
gen t_assistant_female_n = real(t_assistant_female)   

keep if t_all_n != . | t_all == "-"
drop t_all-t_assistant_female
drop if year == 87
save "teachers(88-109).dta", replace

//72-86
use "teachers(72-87)_raw.dta", clear
gen year2 = real(year)
drop year
rename year2 year
gen t_all_n = real(t_all)
gen t_all_male_n = real(t_all_male)
gen t_all_female_n = real(t_all_female)
gen t_professor_male_n = real(t_professor_male)
gen t_professor_female_n = real(t_professor_female)
gen t_associate_male_n = real(t_associate_male)
gen t_associate_female_n = real(t_associate_female)
gen t_assistant_male_n = real(t_assistant_male)
gen t_assistant_female_n = real(t_assistant_female)   

gen sy = year + 1911
gen ey = year + 1920
keep if t_all_n != . | t_all == "-"
drop t_all-t_assistant_female
save "teachers(72-87).dta", replace

//append
use "teachers(88-109).dta", clear
append using "teachers(72-87).dta"
order year sy ey scode sname bcode bname dn t*

//keep if dn == "D" | dn == "D 日間部" | dn == "[D]日間部" | dn == "日" | dn == "日間部" 

rename t_all_n teacher_n
rename t_all_male_n t_male_n
rename t_all_female_n t_female_n

replace bname = subinstr(bname, "　　　　　", "", .)
replace bname = subinstr(bname, "　", "", .)

egen y_sc_bc_bn = concat(year scode bcode bname), punct("-")
egen y_sc_bc = concat(year scode bcode), punct("-")
egen y_sc_bn = concat(year scode bname), punct("-")

// 同一年中，同校裡有相同科系代碼（可能是分組） -> 加總人數
duplicates tag y_sc_bc, gen(ttag)
bysort y_sc_bc: gen tpickone = (_n == 1)
local vars = "teacher_n t_male_n t_female_n t_professor_male_n t_professor_female_n t_associate_male_n t_associate_female_n t_assistant_male_n t_assistant_female_n"
foreach v in `vars' {
	bysort y_sc_bc: egen `v'_temp = total(`v') 
	quietly replace `v' = `v'_temp if ttag & tpickone
}
keep if tpickone
drop *_temp tpickone

// 同一年中，同校裡有相同科系名稱 -> 加總人數
duplicates tag y_sc_bn, gen(ttag2)
bysort y_sc_bn: gen tpickone2 = (_n == 1)
local vars = "teacher_n t_male_n t_female_n t_professor_male_n t_professor_female_n t_associate_male_n t_associate_female_n t_assistant_male_n t_assistant_female_n"
foreach v in `vars' {
	bysort y_sc_bn: egen `v'_temp = total(`v') 
	quietly replace `v' = `v'_temp if ttag2 & tpickone2
}
keep if tpickone2
drop *_temp tpickone2

sort scode bname year
save "teachers.dta", replace

**Merge
use "students.dta", clear
merge 1:1 y_sc_bc using "teachers.dta"

// 把一些同校、科系代碼不同，但其實科系名稱相同的科系撈回來
duplicates tag y_sc_bn, gen(ntag)
bysort y_sc_bn: gen npickone = (_n == 1)
local vars = "student_n s_male_n s_female_n s_m1_n s_f1_n s_m2_n s_f2_n s_m3_n s_f3_n s_m4_n s_f4_n s_m5_n s_f5_n s_m6_n s_f6_n s_m7_n s_f7_n s_m8_n s_f8_n teacher_n t_male_n t_female_n t_professor_male_n t_professor_female_n t_associate_male_n t_associate_female_n t_assistant_male_n t_assistant_female_n"
foreach v in `vars' {
	bysort y_sc_bn: egen `v'_temp = total(`v') 
	quietly replace `v' = `v'_temp if ntag & npickone
}
quietly replace _merge = 3 if ntag & npickone
keep if npickone
drop *_temp npickone

//- students (using) only ：資料的問題、71年前沒有教師的資料
//- teachers (master) only：通常是研究所、院、校長、其他處室等 -> drop掉
drop if _merge == 2
drop if bname == ""

// 把第三、四版代碼變成第五版
quietly include "bcode to 5.do"
duplicates report scode bcode year

egen ID = concat(scode bcode), punct("-")
order ID, before(bname)
sort scode bcode bname year

//檢查區
egen y_sn_bn = concat(year sname bn), punct("-")
egen sc_bc = concat(scode bcode), punct("-")
duplicates tag year scode bcode, gen(t)
tab t
bysort sc_bc:egen t2 = total(t)
sort scode bcode year bname

set more on
list y_sn_bn change possible possible_bcode possible_score possible_sngap possible_tngap possible_n student_n teacher_n, sepby(bcode) noob string(35)
list y_sn_bn change possible possible_bcode possible_score possible_sngap possible_tngap possible_n student_n teacher_n if disappear , sepby(bcode) noob string(35) 
list y_sn_bn change possible possible_bcode possible_score possible_sngap possible_tngap possible_n student_n teacher_n if disappear & change & possible_score != 100, sepby(scode bcode) noob string(35)
list y_sn_bn change possible possible_bcode possible_score possible_sngap possible_tngap possible_n student_n teacher_n if disappear & !change & possible_score != 100, sepby(bcode) noob string(35) 
set more off

egen sc_bc1 = tag(sc_bc)
randomtag if sc_bc1, count(30) gen(s)
bysort sc_bc: egen select = total(s)
list y_sn_bn change possible possible_bcode possible_score possible_sngap possible_tngap possible_n student_n teacher_n if select, sepby(bcode) noob string(35)

save "college_clean", replace

*=====Start Analysis!!!=======================================================================================*

use "college_clean", clear

merge m:1 year using "graduate.dta", nogen
replace high_graduate_n = high_graduate_n
gen lnhigh_graduate_n = ln(high_graduate_n)
gen lnhigh_graduate_n_3pmean = ln(high_graduate_n_3pmean)

destring scode , gen(scode1)
gen public = int(scode1/1000)
label define public 0 "國立" 1 "私立" 2 "省立" 3 "市立"
label value public public

recode public (0 2 3=1)(1=2), gen(sctype)
label define sctype 1 "公立" 2 "私立"
label value sctype sctype

gen scway1 = int((scode1 - public*1000)/100)
recode scway1 (0=1)(1=2)
label define scway 1"一般大學" 2"技專院校"
label value scway scway

egen y_sn_bn = concat(year sname bn), punct("-")
egen sc_bc = concat(scode bcode), punct("-")
egen y_sc = concat(year scode), punct("-")

// 同一年中，有相同學校－科系代碼的，drop掉（來自於資料處理錯誤）
duplicates tag year scode bcode, gen(t)
tab t
bysort sc_bc: egen t2 = total(t)
tab t2
drop if t2 

quietly include "bcode transform.do"
drop if bcode1_new == .

// 定義科系消失1: bocde消失
bysort sc_bc: egen start = min(year)
bysort sc_bc: egen end = max(year)
gen age = year - start + 1
gen disbanding0 = end == year 
replace disbanding0 = 0 if year == 109 

egen s1 = rowtotal(s_m1_n s_f1_n)
bysort sc_bc: egen hasd = sum(disbanding0)
gen disbanding = 0
replace disbanding = 1 if s1 == 0 & hasd

stset age, id(sc_bc) failure(disbanding)  
keep if _st

//tab year disbanding
//graph bar (sum) disbanding, over(sy)
//graph bar (count) disbanding, over(sy)

/*
preserve
collapse (count) disbanding, by(year bcode1_new)
sepscatter disbanding year , sep(bcode1_new) recast(connect) legend(size(vsmall) col(3)) 
restore
*/

ltable _t0 disbanding , tvid(sc_bc) noadjust
ltable _t0 disbanding , tvid(sc_bc) hazard noadjust

/*
preserve
ltable _t0 disbanding, tvid(sc_bc) i(1) noadjust graph yline(0.5, lwidth(thin) lcolor(gs10)) 
tempfile hazard
quietly ltable _t0 disbanding, tvid(sc_bc) i(1) saving(`hazard')
use `hazard', clear
twoway connected haz t0
restore
*/

egen sctype_way = concat(sctype scway)
encode sctype_way, gen(sctype_way_temp)
drop sctype_way
rename sctype_way_temp sctype_way
lab define sctype_way 1"公立一般大學" 2"公立技專校院" 3"私立一般大學" 4"私立技專校院"
lab value sctype_way sctype_way

//sts graph, by(sctype_way)
//sts graph, by(bcode1_new)

gen age2 = age * age
gen lnage = ln(age)

bysort year: egen Nt = count(year)
gen Nt2 = Nt^2 / 1000

bysort y_sc: egen Nst = count(year)
gen Nst2 = Nst^2 / 1000

bysort bcode1_new year: egen Nbt = count(year)
gen Nbt2 = Nbt^2 / 1000

bysort bcode2_new year: egen Nb2t = count(year)
gen Nb2t2 = Nb2t^2 / 1000

bysort y_sc: egen SNst = sum(student_n)
gen SNst2 = SNst^2 / 100000

bysort bcode1_new year: egen SNbt = sum(student_n)
gen SNbt2 = SNbt^2 / 100000

bysort bcode2_new year: egen SNb2t = sum(student_n)
gen SNb2t2 = SNb2t^2 / 100000


bysort scode year:egen school_field_per = mean(field2)
replace school_field_per = (school_field_per - 1)*100
gen school_field = school_field_per < 50
lab define school_field 0"偏向理組"1"偏向文組"
lab value school_field school_field

gen y = sy - 1972
gen y2 = y*y

recode s_*_n (. = 0)

recode sy (1972/1985=1)(1986/1997=2)(1998/2012=3)(2013/2020=4), gen(period)

sort sc_bc year

forvalues x = 1(1)8 {
	gen s`x'_n = s_m`x'_n + s_f`x'_n
	gen s`x'_np = s`x'_n
	bysort sc_bc: replace s`x'_np = s`x'_n[_n-1] if _t != 1
}

gen s8_per = .
local N = _N
forvalues i = 1/`N' {
	forvalues x = 7(-1)1{
		if (s8_per[`i'] == . & s`x'_np[`i'] > 6 &  s`x'_n[`i'] > 3) {
			qui replace s8_per = (s8_n / s`x'_np) * 100 in `i'
		}
	}
}
recode s8_per (.=0)
replace s8_per = 100 if s8_per > 130
gen s8_per2 = (s8_n / student_n) * 100

recode t_professor_male_n t_professor_female_n t_associate_male_n t_associate_female_n t_assistant_male_n t_assistant_female_n (.=0)
gen othert_per = (1 - (t_professor_male_n + t_professor_female_n + t_associate_male_n + t_associate_female_n + t_assistant_male_n + t_assistant_female_n) / teacher_n)*100

gen lnstudent_n = ln(student_n)
gen student_np = student_n
sort sc_bc year
bysort sc_bc: replace student_np = student_n[_n-1] if _t != 1
gen student_n_gap = (student_n - student_np) / student_np * 100

bysort y_sc bcode2_new: gen b2_per = _N 
by y_sc: replace b2_per = 100 * b2_per / _N 

gen lnSNst = ln(SNst)
gen gradurate_rate = high_graduate_n / Nt

save "outcome.dta", replace

//Descriptive statistics
sort sc_bc year
bysort scode: gen spick = _n == _N  
bysort sc_bc: gen bpick = _n == _N 

sum lnstudent_n s8_per if lnstudent_n != .
tab period if lnstudent_n != .
tab field2 if bpick
tab sctype if spick
tab scway if spick
tab school_field if spick

//Models (Multilevel Discrete-time Survival Analysis)
/*
L1: [age lnage age2] [文理組 領域 學門] 學生數量t 延畢率t(兩種) [Nt Nst Nbt Nb2t] [年 period]
L2: 公私立 大學或技專 區域 文理組比例  [SNst Nst]
*/

est clear
qui {
melogit disbanding || scode:
est store m1
melogit disbanding age lnstudent_n s8_per i.field2 i.period || scode: 
est store m2
melogit disbanding age Nb2t Nb2t2 lnstudent_n s8_per i.field2 i.period || scode: 
est store m3
melogit disbanding age Nb2t Nb2t2 lnstudent_n s8_per i.field2##i.school_field i.period i.sctype i.scway|| scode: 
est store m4
}
esttab m2 m3 m4 using "models.csv",  cells(b(star fmt(3)) se(par fmt(2))) stats(ll N) nobase compress replace

/*
graph bar (count) disbanding, over(sy)
graph bar (sum) disbanding, over(sy)

sts graph
sts graph, by(field2)
sts test field2 
stci, by(field2) median
sts graph, by(sctype)
sts test sctype 
sts graph, by(scway)
*/
