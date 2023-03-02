
clonevar bcode_raw = bcode

gen bcode_to5 = substr(bcode, 1, 4) if year < 106
gen bcode_to5_temp =  substr(bcode, 1, 5) if year >= 106
replace bcode_to5 = bcode_to5_temp if bcode_to5 == ""
drop bcode_to5_temp

gen bcode_back = substr(bcode, 5, 6) if year < 106
gen bcode_back_temp =  substr(bcode, 6, 8) if year >= 106
replace bcode_back = bcode_back_temp if bcode_back == ""
drop bcode_back_temp

clonevar bcode_to5_raw = bcode_to5

//85 -> 96年
replace bcode_to5 = "2101" if bcode_to5 == "1804" & year <= 95
replace bcode_to5 = "2102" if bcode_to5 == "1808" & year <= 95
replace bcode_to5 = "2103" if bcode_to5 == "1812" & year <= 95
replace bcode_to5 = "2104" if bcode_to5 == "1822" & year <= 95
replace bcode_to5 = "2105" if bcode_to5 == "1832" & year <= 95
replace bcode_to5 = "2106" if bcode_to5 == "1842" & year <= 95
replace bcode_to5 = "2107" if bcode_to5 == "1852" & year <= 95
replace bcode_to5 = "2201" if bcode_to5 == "2211" & year <= 95
replace bcode_to5 = "2203" if bcode_to5 == "2215" & year <= 95
replace bcode_to5 = "2207" if bcode_to5 == "2231" & year <= 95
replace bcode_to5 = "2209" if bcode_to5 == "2251" & year <= 95
replace bcode_to5 = "2210" if bcode_to5 == "2261" & year <= 95
replace bcode_to5 = "2211" if bcode_to5 == "2271" & year <= 95
replace bcode_to5 = "3101" if bcode_to5 == "3012" & year <= 95
replace bcode_to5 = "3102" if bcode_to5 == "3022" & year <= 95
replace bcode_to5 = "3102" if bcode_to5 == "3022" & year <= 95
replace bcode_to5 = "3103" if bcode_to5 == "3032" & year <= 95
replace bcode_to5 = "3104" if bcode_to5 == "3042" & year <= 95
replace bcode_to5 = "3105" if bcode_to5 == "3052" & year <= 95
replace bcode_to5 = "3106" if bcode_to5 == "3062" & year <= 95
replace bcode_to5 = "3107" if bcode_to5 == "3072" & year <= 95
replace bcode_to5 = "3108" if bcode_to5 == "3452" & year <= 95
replace bcode_to5 = "3201" if bcode_to5 == "8401" & year <= 95
replace bcode_to5 = "3202" if bcode_to5 == "8402" & year <= 95
replace bcode_to5 = "3203" if bcode_to5 == "8404" & year <= 95
replace bcode_to5 = "3204" if bcode_to5 == "8407" & year <= 95
replace bcode_to5 = "3206" if bcode_to5 == "8422" & year <= 95
replace bcode_to5 = "3207" if bcode_to5 == "8425" & year <= 95
replace bcode_to5 = "3299" if bcode_to5 == "8499" & year <= 95
replace bcode_to5 = "3402" if bcode_to5 == "3428" & year <= 95
replace bcode_to5 = "3403" if bcode_to5 == "3434" & year <= 95
replace bcode_to5 = "3404" if bcode_to5 == "3435" & year <= 95
replace bcode_to5 = "3405" if bcode_to5 == "3436" & year <= 95
replace bcode_to5 = "3406" if bcode_to5 == "3437" & year <= 95
replace bcode_to5 = "4201" if bcode_to5 == "4202" & year <= 95
replace bcode_to5 = "4401" if bcode_to5 == "4212" & year <= 95
replace bcode_to5 = "4402" if bcode_to5 == "4222" & year <= 95
replace bcode_to5 = "4403" if bcode_to5 == "4232" & year <= 95
replace bcode_to5 = "4404" if bcode_to5 == "4252" & year <= 95
replace bcode_to5 = "4405" if bcode_to5 == "4262" & year <= 95
replace bcode_to5 = "4499" if bcode_to5 == "4299" & year <= 95
replace bcode_to5 = "4801" if bcode_to5 == "4641" & year <= 95
replace bcode_to5 = "5201" if bcode_to5 == "5422" & year <= 95
replace bcode_to5 = "5202" if bcode_to5 == "5442" & year <= 95
replace bcode_to5 = "5203" if bcode_to5 == "5416" & year <= 95
replace bcode_to5 = "5204" if bcode_to5 == "5412" & year <= 95
replace bcode_to5 = "5205" if bcode_to5 == "5414" & year <= 95
replace bcode_to5 = "5206" if bcode_to5 == "5426" & year <= 95
replace bcode_to5 = "5207" if bcode_to5 == "5474" & year <= 95
replace bcode_to5 = "5208" if bcode_to5 == "5402" & year <= 95
replace bcode_to5 = "5209" if bcode_to5 == "5418" & year <= 95
replace bcode_to5 = "5210" if bcode_to5 == "5420" & year <= 95
replace bcode_to5 = "5212" if bcode_to5 == "5476" & year <= 95
replace bcode_to5 = "5299" if bcode_to5 == "5499" & year <= 95
replace bcode_to5 = "6401" if bcode_to5 == "6232" & year <= 95
replace bcode_to5 = "7201" if bcode_to5 == "5006" & year <= 95
replace bcode_to5 = "7202" if bcode_to5 == "5002" & year <= 95
replace bcode_to5 = "7203" if bcode_to5 == "5052" & year <= 95
replace bcode_to5 = "7204" if bcode_to5 == "5008" & year <= 95
replace bcode_to5 = "7205" if bcode_to5 == "6612" & year <= 95
replace bcode_to5 = "7206" if bcode_to5 == "5012" & year <= 95
replace bcode_to5 = "7207" if bcode_to5 == "5030" & year <= 95
replace bcode_to5 = "7208" if bcode_to5 == "5042" & year <= 95
replace bcode_to5 = "7299" if bcode_to5 == "5099" & year <= 95
replace bcode_to5 = "7604" if bcode_to5 == "6622" & year <= 95
replace bcode_to5 = "8101" if bcode_to5 == "7822" & year <= 95
replace bcode_to5 = "8102" if bcode_to5 == "7872" & year <= 95
replace bcode_to5 = "8103" if bcode_to5 == "8962" & year <= 95
replace bcode_to5 = "8106" if bcode_to5 == "6601" & year <= 95
replace bcode_to5 = "8107" if bcode_to5 == "7812" & year <= 95
replace bcode_to5 = "8199" if bcode_to5 == "6699" & year <= 95
replace bcode_to5 = "8401" if bcode_to5 == "7001" & year <= 95
replace bcode_to5 = "8402" if bcode_to5 == "7002" & year <= 95
replace bcode_to5 = "8403" if bcode_to5 == "7004" & year <= 95
replace bcode_to5 = "8499" if bcode_to5 == "7099" & year <= 95
replace bcode_to5 = "8601" if bcode_to5 == "8913" & year <= 95
replace bcode_to5 = "8602" if bcode_to5 == "8919" & year <= 95
replace bcode_to5 = "9901" if bcode_to5 == "8999" & year <= 95
replace bcode_to5 = "1401" if bcode_to5 == "1401" & year <= 95
replace bcode_to5 = "1402" if bcode_to5 == "1404" & year <= 95
replace bcode_to5 = "1403" if bcode_to5 == "1408" & year <= 95
replace bcode_to5 = "1404" if bcode_to5 == "1412" & year <= 95
replace bcode_to5 = "1499" if bcode_to5 == "1499" & year <= 95
replace bcode_to5 = "2299" if bcode_to5 == "2299" & year <= 95
replace bcode_to5 = "3401" if bcode_to5 == "3401" & year <= 95
replace bcode_to5 = "3499" if bcode_to5 == "3499" & year <= 95
replace bcode_to5 = "3801" if bcode_to5 == "3801" & year <= 95
replace bcode_to5 = "3899" if bcode_to5 == "3899" & year <= 95
replace bcode_to5 = "4601" if bcode_to5 == "4601" & year <= 95
replace bcode_to5 = "4602" if bcode_to5 == "4611" & year <= 95
replace bcode_to5 = "4699" if bcode_to5 == "4699" & year <= 95
replace bcode_to5 = "5801" if bcode_to5 == "5801" & year <= 95
replace bcode_to5 = "5802" if bcode_to5 == "5812" & year <= 95
replace bcode_to5 = "5803" if bcode_to5 == "5822" & year <= 95
replace bcode_to5 = "5899" if bcode_to5 == "5899" & year <= 95
replace bcode_to5 = "6201" if bcode_to5 == "6201" & year <= 95
replace bcode_to5 = "6202" if bcode_to5 == "6203" & year <= 95
replace bcode_to5 = "6203" if bcode_to5 == "6206" & year <= 95
replace bcode_to5 = "6204" if bcode_to5 == "6208" & year <= 95
replace bcode_to5 = "6205" if bcode_to5 == "6212" & year <= 95
replace bcode_to5 = "6206" if bcode_to5 == "6222" & year <= 95
replace bcode_to5 = "6207" if bcode_to5 == "6226" & year <= 95
replace bcode_to5 = "6208" if bcode_to5 == "6230" & year <= 95
replace bcode_to5 = "6210" if bcode_to5 == "6262" & year <= 95
replace bcode_to5 = "6211" if bcode_to5 == "6272" & year <= 95
replace bcode_to5 = "6299" if bcode_to5 == "6299" & year <= 95

gen bcode_3to4 = 0
foreach b in "2101" "2102" "2103" "2104" "2105" "2106" "2107" "2201" "2203" "2207" "2209" "2210" "2211" "3101" "3102" "3103" "3104" "3105" "3106" "3107" "3108" "3201" "3202" "3203" "3204" "3206" "3207" "3299" "3402" "3403" "3404" "3405" "3406" "4201" "4401" "4402" "4403" "4404" "4405" "4499" "4801" "5201" "5202" "5203" "5204" "5205" "5206" "5207" "5208" "5209" "5210" "5212" "5299" "6401" "7201" "7202" "7203" "7204" "7205" "7206" "7207" "7208" "7299" "7604" "8101" "8102" "8103" "8106" "8107" "8199" "8401" "8402" "8403" "8499" "8601" "8602" "9901" "1401" "1402" "1403" "1404" "1499" "2299" "3401" "3499" "3801" "3899" "4601" "4602" "4699" "5801" "5802" "5803" "5899" "6201" "6202" "6203" "6204" "6205" "6206" "6207" "6208" "6210" "6211" "6299"  {
	replace bcode_3to4 = 1 if bcode_to5 == "`b'"
}

//96 -> 106年
replace bcode_to5  = "01111" if bcode_to5 == "1401" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01112" if bcode_to5 == "1405" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01113" if bcode_to5 == "1406" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01114" if bcode_to5 == "1407" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01116" if bcode_to5 == "1408" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01117" if bcode_to5 == "1409" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01121" if bcode_to5 == "1404" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01131" if bcode_to5 == "1402" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01141" if bcode_to5 == "1403" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "01199" if bcode_to5 == "1499" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02111" if bcode_to5 == "2106" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02112" if bcode_to5 == "2302" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02121" if bcode_to5 == "2109" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02122" if bcode_to5 == "2301" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02123" if bcode_to5 == "2303" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02124" if bcode_to5 == "2304" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02125" if bcode_to5 == "8107" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02131" if bcode_to5 == "2101" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02132" if bcode_to5 == "2102" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02141" if bcode_to5 == "2103" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02142" if bcode_to5 == "2108" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02151" if bcode_to5 == "2104" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02152" if bcode_to5 == "2105" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02191" if bcode_to5 == "2107" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02192" if bcode_to5 == "2110" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02199" if bcode_to5 == "2399" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02211" if bcode_to5 == "2208" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02221" if bcode_to5 == "2209" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02222" if bcode_to5 == "2210" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02223" if bcode_to5 == "2212" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02231" if bcode_to5 == "2211" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02299" if bcode_to5 == "2299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02311" if bcode_to5 == "2203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02312" if bcode_to5 == "2205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02321" if bcode_to5 == "2201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02322" if bcode_to5 == "2202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "02399" if bcode_to5 == "2204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03111" if bcode_to5 == "3101" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03121" if bcode_to5 == "3102" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03122" if bcode_to5 == "3109" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03131" if bcode_to5 == "3105" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03141" if bcode_to5 == "3103" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03142" if bcode_to5 == "3106" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03143" if bcode_to5 == "3107" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03199" if bcode_to5 == "3110" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03211" if bcode_to5 == "3201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03212" if bcode_to5 == "3202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03213" if bcode_to5 == "3203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03214" if bcode_to5 == "3207" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03221" if bcode_to5 == "3205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03222" if bcode_to5 == "3206" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "03299" if bcode_to5 == "3299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04111" if bcode_to5 == "3402" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04121" if bcode_to5 == "3405" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04122" if bcode_to5 == "3407" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04123" if bcode_to5 == "3406" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04131" if bcode_to5 == "3403" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04132" if bcode_to5 == "3408" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04133" if bcode_to5 == "3409" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04134" if bcode_to5 == "3108" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04141" if bcode_to5 == "3404" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04142" if bcode_to5 == "3204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04143" if bcode_to5 == "3208" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04191" if bcode_to5 == "3401" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04199" if bcode_to5 == "3499" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04211" if bcode_to5 == "3801" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04212" if bcode_to5 == "3802" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "04299" if bcode_to5 == "3899" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05111" if bcode_to5 == "4201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05121" if bcode_to5 == "4203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05122" if bcode_to5 == "4204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05123" if bcode_to5 == "4205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05124" if bcode_to5 == "4206" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05191" if bcode_to5 == "7205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05199" if bcode_to5 == "4299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05211" if bcode_to5 == "8501" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05212" if bcode_to5 == "4202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05291" if bcode_to5 == "8502" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05292" if bcode_to5 == "6207" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05299" if bcode_to5 == "8599" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05311" if bcode_to5 == "4401" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05321" if bcode_to5 == "4402" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05322" if bcode_to5 == "4404" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05323" if bcode_to5 == "4405" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05331" if bcode_to5 == "4403" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05332" if bcode_to5 == "4406" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05399" if bcode_to5 == "4499" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05411" if bcode_to5 == "4601" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05421" if bcode_to5 == "4602" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "05499" if bcode_to5 == "4699" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06121" if bcode_to5 == "4802" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06131" if bcode_to5 == "4801" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06132" if bcode_to5 == "4803" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06133" if bcode_to5 == "4804" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06134" if bcode_to5 == "4805" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "06199" if bcode_to5 == "4899" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07111" if bcode_to5 == "5204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07112" if bcode_to5 == "5205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07121" if bcode_to5 == "5209" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07122" if bcode_to5 == "5210" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07131" if bcode_to5 == "5212" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07141" if bcode_to5 == "5201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07151" if bcode_to5 == "5202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07191" if bcode_to5 == "5206" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07192" if bcode_to5 == "5207" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07193" if bcode_to5 == "5211" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07194" if bcode_to5 == "5213" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07199" if bcode_to5 == "5299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07211" if bcode_to5 == "6206" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07311" if bcode_to5 == "5801" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07312" if bcode_to5 == "5802" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07313" if bcode_to5 == "5803" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07321" if bcode_to5 == "5203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07322" if bcode_to5 == "5208" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "07399" if bcode_to5 == "5899" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08111" if bcode_to5 == "6201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08112" if bcode_to5 == "6202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08121" if bcode_to5 == "6203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08191" if bcode_to5 == "6208" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08192" if bcode_to5 == "6209" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08193" if bcode_to5 == "6205" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08194" if bcode_to5 == "6204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08199" if bcode_to5 == "6299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08211" if bcode_to5 == "6210" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08311" if bcode_to5 == "6211" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "08411" if bcode_to5 == "6401" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09111" if bcode_to5 == "7208" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09121" if bcode_to5 == "7201" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09131" if bcode_to5 == "7206" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09141" if bcode_to5 == "7207" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09159" if bcode_to5 == "7204" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09161" if bcode_to5 == "7203" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09191" if bcode_to5 == "7202" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09199" if bcode_to5 == "7299" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09211" if bcode_to5 == "7602" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09212" if bcode_to5 == "7601" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09221" if bcode_to5 == "7604" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09231" if bcode_to5 == "7603" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "09299" if bcode_to5 == "7699" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10111" if bcode_to5 == "8106" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10121" if bcode_to5 == "8108" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10131" if bcode_to5 == "8101" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10141" if bcode_to5 == "8103" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10142" if bcode_to5 == "8104" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10151" if bcode_to5 == "8102" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10152" if bcode_to5 == "8105" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10199" if bcode_to5 == "8199" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10321" if bcode_to5 == "8601" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10411" if bcode_to5 == "8401" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10413" if bcode_to5 == "8402" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10414" if bcode_to5 == "8403" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "10499" if bcode_to5 == "8499" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))
replace bcode_to5  = "99999" if bcode_to5 == "9901" & ((year >= 96 & year <= 105) | (year <= 95 & bcode_3to4))

replace bcode = bcode_to5
drop bcode_to5_raw bcode_3to4
rename bcode_to5 bcode_to5_raw

sort scode bname year
egen sc_bn = concat(scode bname), punct("-")
clonevar bcode_back2 = bcode_back
replace bcode_back = "" if length(bcode_back) != 3
replace bcode_back2 = "" if length(bcode_back2) != 2
bysort sc_bn: replace bcode_back = bcode_back[_N] if bcode_back == ""
bysort sc_bn: replace bcode_back2 = bcode_back2[_N] if bcode_back2 == ""

egen bcode_temp = concat(bcode bcode_back), punct("")
replace bcode = bcode_temp if bcode_back != ""
egen bcode_temp2 = concat(bcode bcode_back2), punct("")
replace bcode = bcode_temp2 if bcode_back == ""
drop bcode_temp bcode_temp2

egen bcode_temp = concat(bcode bcode_raw), punct("-")
replace bcode = bcode_temp if t
drop t bcode_temp

replace bcode_to5_raw = bcode

order bcode_raw bcode_to5_raw bcode_back*, before(bcode)
