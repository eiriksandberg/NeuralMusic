import matplotlib.pyplot as plt
import numpy as np

a = [0.00763256149366498, 0.00691147381439805, 0.006680745631456375, 0.006572807673364878, 0.00652454374358058, 0.0064745331183075905, 0.006421636790037155, 0.006385934539139271, 0.006254411768168211, 0.006325790658593178, 0.006318940315395594, 0.006251323036849499, 0.006271834950894117, 0.00619552843272686, 0.0062050288543105125, 0.006155061069875956, 0.006201154552400112, 0.006195022724568844, 0.006176532246172428, 0.006219132803380489, 0.006117051467299461, 0.0061865681782364845, 0.006112187635153532, 0.006115692667663097, 0.006089100614190102, 0.006195370107889175, 0.00607666838914156, 0.006016709376126528, 0.006077939178794622, 0.006056403275579214, 0.005950218066573143, 0.0060862344689667225, 0.005995102226734161, 0.005967399105429649, 0.005949350539594889, 0.005899778101593256, 0.005849818699061871, 0.005972785875201225, 0.0058394926600158215, 0.005985406693071127, 0.005884367041289806, 0.005963786039501429, 0.0058443923480808735, 0.005920228082686663, 0.00586145743727684, 0.005996049847453833, 0.005791814066469669, 0.005809288006275892, 0.0058543807826936245, 0.005772660952061415, 0.0058456724509596825, 0.005804955027997494, 0.00587223656475544, 0.005823339801281691, 0.00569544592872262, 0.005698501598089933, 0.005586155690252781, 0.005741072352975607, 0.0055824280716478825, 0.0056692203506827354, 0.005686663556843996, 0.005769194569438696, 0.005819027312099934, 0.005710523575544357, 0.005810532718896866, 0.005732550751417875, 0.005672995932400227, 0.005727833136916161, 0.005885686259716749, 0.005899977404624224, 0.005627327132970095, 0.005650701932609081, 0.005579774733632803, 0.005554654635488987, 0.005633424501866102, 0.005624340381473303, 0.005662643350660801, 0.005667720455676317, 0.005591895431280136, 0.00560265826061368, 0.005598084535449743, 0.005445182789117098, 0.00567989656701684, 0.005565309431403875, 0.0057672481052577496, 0.005662286188453436, 0.005712966434657574, 0.005627259146422148, 0.005566871725022793, 0.00553187495097518, 0.005632647778838873, 0.0057412246242165565, 0.005494250450283289, 0.005647317506372929, 0.0055490112863481045, 0.006420654244720936, 0.005689559504389763, 0.005488415714353323, 0.005456401500850916, 0.005438459571450949]

b = [0.007918252609670162, 0.007067665923386812, 0.006772743538022041, 0.006709948182106018, 0.006570881232619286, 0.00655344920232892, 0.006498181726783514, 0.006612216122448444, 0.006383134517818689, 0.006386579945683479, 0.0064600142650306225, 0.0063287862576544285, 0.006311924196779728, 0.006315553095191717, 0.006296646781265736, 0.006314867176115513, 0.006308392155915499, 0.006318966392427683, 0.00626926776021719, 0.006342435255646706, 0.006278947927057743, 0.006237734574824572, 0.006240335293114185, 0.0062470207922160625, 0.006179029121994972, 0.006135334726423025, 0.006068137474358082, 0.006053006276488304, 0.006319486070424318, 0.006630612071603537, 0.006112290546298027, 0.00610974570736289, 0.005976833403110504, 0.006056586746126413, 0.0061363899149000645, 0.006010618060827255, 0.006254015956073999, 0.0061276750639081, 0.006038654129952192, 0.0060464139096438885, 0.006043362431228161, 0.006128956563770771, 0.0060121165588498116, 0.006016592029482126, 0.0061014797538518906, 0.006061915308237076, 0.00629523815587163, 0.005935920402407646, 0.00600783945992589, 0.006068292539566755, 0.00602878350764513, 0.006023526657372713, 0.005970875266939402, 0.006143887527287006, 0.005911499261856079, 0.005974088795483112, 0.006003745831549168, 0.0059531996957957745, 0.005984482355415821, 0.006045794580131769, 0.005956436973065138, 0.006007698830217123, 0.006008149590343237, 0.005904592107981443, 0.005883879028260708, 0.006030169781297445, 0.006087931804358959, 0.0059424820356070995, 0.006015571299940348, 0.005872523877769709, 0.00596616929396987, 0.006550850346684456, 0.006151814479380846, 0.006057367660105228, 0.005932135507464409, 0.005783812142908573, 0.005918120499700308, 0.0058840359561145306, 0.0059125120751559734, 0.005897621624171734, 0.006024932488799095, 0.0058282604441046715, 0.00594251649454236, 0.005917075555771589, 0.005943864118307829, 0.005925824400037527, 0.005908865015953779, 0.006139702629297972, 0.005851134192198515, 0.005879067815840244, 0.005826009903103113, 0.00581516046077013, 0.006123463157564402, 0.0058333077467978, 0.005938129965215921, 0.005864563398063183, 0.005948101170361042, 0.005922902375459671, 0.006042606197297573, 0.005849645938724279]

c = [0.0076178801245987415, 0.007211647462099791, 0.007033040281385183, 0.0069308215752244, 0.006835035979747772, 0.0067911832593381405, 0.006732835900038481, 0.006700990721583366, 0.006732848938554525, 0.006612813100218773, 0.006617305334657431, 0.006507979705929756, 0.006582221016287804, 0.00653226999565959, 0.006476094014942646, 0.006431650836020708, 0.006522521376609802, 0.006480433978140354, 0.006436522584408522, 0.006500015966594219, 0.006297766231000423, 0.006470445543527603, 0.0063926298171281815, 0.0062613897025585175, 0.006392940413206816, 0.006252252031117678, 0.006350174080580473, 0.006179017946124077, 0.006223205476999283, 0.006154729053378105, 0.006059139501303434, 0.006206797435879707, 0.006097746547311544, 0.006091043818742037, 0.0061681438237428665, 0.006057269871234894, 0.00612249318510294, 0.006066020578145981, 0.00606156699359417, 0.006047147326171398, 0.0059879859909415245, 0.006175340618938208, 0.006008548196405172, 0.005982742179185152, 0.006100427359342575, 0.00607629818841815, 0.006078434642404318, 0.0060426462441682816, 0.005976318381726742, 0.005924702621996403, 0.00601424602791667, 0.0060978480614721775, 0.005901044700294733, 0.005905449856072664, 0.005952489096671343, 0.006021014414727688, 0.005786063149571419, 0.00607737572863698, 0.006017062813043594, 0.005875597707927227, 0.005958087742328644, 0.0059449695982038975, 0.005978119559586048, 0.00586274778470397, 0.005938780959695578, 0.005839208606630564, 0.005971824750304222, 0.005939194466918707, 0.00591265456750989, 0.00589511264115572, 0.005839315243065357, 0.005884973797947168, 0.0059221223928034306, 0.005768917500972748, 0.005802367348223925, 0.005963522475212812, 0.005841679871082306, 0.005823621992021799, 0.005924562457948923, 0.005906255450099707, 0.005819563288241625, 0.005852440372109413, 0.005721868481487036, 0.005798181053251028, 0.005830432754009962, 0.005793026182800531, 0.005936610512435436, 0.005804417189210653, 0.005818242207169533, 0.0058143301866948605, 0.0056748343631625175, 0.00591264059767127, 0.005761194042861462, 0.005744014400988817, 0.005724865011870861, 0.005795888602733612, 0.005788292270153761, 0.005830188747495413, 0.00577711733058095, 0.005828239023685455]

plt.plot(a)
plt.plot(b)
plt.plot(c)
plt.legend(['Dim = 15', 'Dim = 30', 'Dim = 45'], loc='upper right')
plt.show()