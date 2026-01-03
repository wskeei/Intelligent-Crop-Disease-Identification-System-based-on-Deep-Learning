export interface Disease {
    id: string;
    name: string;
    category: string;
    icon: string;
    description: string;
    severity: string;
    severityLevel: 'high' | 'medium' | 'low';
    symptoms: string[];
    causes: string[];
    prevention: string[];
    treatment: string[];
    images: string[];
}

export const diseases: Disease[] = [
    {
        id: 'apple_scab',
        name: '苹果黑星病',
        category: '真菌病害',
        icon: '🍎',
        description: '苹果黑星病是苹果生产中最具破坏性的真菌病害之一，主要危害叶片和果实，导致果实畸形、开裂，叶片早落。',
        severity: '高风险',
        severityLevel: 'high',
        symptoms: [
            '叶片初生黄绿色斑点，渐变为黑褐色霉斑',
            '果实出现圆形黑色凹陷斑点，表面往往龟裂',
            '严重时造成大量落叶、落果',
            '果实受害后变成畸形果，不耐贮藏'
        ],
        causes: [
            '低温高湿环境有利于病菌繁殖',
            '春季降雨频繁',
            '果园通风透光不良',
            '树势衰弱，管理粗放'
        ],
        prevention: [
            '选用抗病品种',
            '秋冬季由于扫除落叶，集中烧毁',
            '合理修剪，改善通风透光条件',
            '加强肥水管理，增强树势'
        ],
        treatment: [
            '发病初期喷洒波尔多液',
            '使用氟硅唑、腈菌唑等杀菌剂防治',
            '每隔10-15天喷药一次，连续防治3-4次'
        ],
        images: [] // Placeholder for real image URLs
    },
    {
        id: 'corn_common_rust',
        name: '玉米普通锈病',
        category: '真菌病害',
        icon: '🌽',
        description: '主要发生在玉米生长中后期，严重影响光合作用，造成减产。病原菌随气流传播，扩散速度快。',
        severity: '中风险',
        severityLevel: 'medium',
        symptoms: [
            '叶片两面产生圆形或长圆形隆起的锈褐色斑点（夏孢子堆）',
            '后期表皮破裂，散出锈色粉末',
            '严重时叶片干枯死亡',
            '籽粒干瘪，产量下降'
        ],
        causes: [
            '气温在16-23℃且湿度高时易发病',
            '偏施氮肥，植株疯长',
            '连作地块菌源积累多'
        ],
        prevention: [
            '种植抗病品种',
            '适时播种，避开病害高发期',
            '合理密植，清洁田园'
        ],
        treatment: [
            '发病初期喷施三唑酮、戊唑醇',
            '间隔7-10天喷药一次'
        ],
        images: []
    },
    {
        id: 'grape_black_rot',
        name: '葡萄黑腐病',
        category: '真菌病害',
        icon: '🍇',
        description: '葡萄主要病害之一，主要危害果实，也能侵害叶片和新梢。果实发病后迅速腐烂、干缩成僵果。',
        severity: '高风险',
        severityLevel: 'high',
        symptoms: [
            '果实出现紫褐色小斑点，迅速扩大波及全果',
            '病果变软腐烂，随后干缩成黑色僵果',
            '叶片出现红褐色病斑，边缘有深褐色晕圈',
            '僵果经冬不落'
        ],
        causes: [
            '高温多雨季节最易发病',
            '果园地势低洼，排水不良',
            '修剪不及时，架面郁闭'
        ],
        prevention: [
            '彻底清除越冬病源，剪除病枝病果',
            '果实套袋保护',
            '及时绑蔓摘心，利于通风'
        ],
        treatment: [
            '花前花后喷施代森锰锌保护',
            '发病初期使用苯醚甲环唑防治'
        ],
        images: []
    },
    {
        id: 'tomato_bacterial_spot',
        name: '番茄细菌性斑点病',
        category: '细菌病害',
        icon: '🍅',
        description: '由细菌引起的病害，主要危害叶、茎、花、果实。特别是高温多雨年份发生严重。',
        severity: '中风险',
        severityLevel: 'medium',
        symptoms: [
            '叶片产生深褐色至黑色水呈状小斑点',
            '由于病斑周围有黄色晕圈',
            '果实表面产生黑色隆起小斑点（疮痂状）',
            '严重时引起落叶、落花、落果'
        ],
        causes: [
            '种子带菌',
            '高温高湿环境（25-30℃）',
            '通过雨水飞溅或农事操作传播'
        ],
        prevention: [
            '种子温汤浸种消毒',
            '实行轮作，避免连作',
            '采用地膜覆盖，减少土壤病菌飞溅'
        ],
        treatment: [
            '发病初期喷洒氢氧化铜、链霉素',
            '注意交替用药，防止产生抗药性'
        ],
        images: []
    },
    {
        id: 'potato_early_blight',
        name: '马铃薯早疫病',
        category: '真菌病害',
        icon: '🥔',
        description: '主要侵染叶片，也可危害块茎。病斑具同心轮纹，俗称"轮纹病"。',
        severity: '低风险',
        severityLevel: 'low',
        symptoms: [
            '叶片产生圆形或近圆形黑褐色病斑',
            '病斑具明显的同心轮纹',
            '潮湿时病斑上生黑色霉层',
            '发病重时叶片干枯脱落'
        ],
        causes: [
            '植株生长衰弱期易感病',
            '高温干旱与高湿交替环境',
            '缺肥、生长不良地块发病重'
        ],
        prevention: [
            '加强肥水管理，防止植株早衰',
            '配方施肥，增施磷钾肥',
            '清洁田园，销毁病残体'
        ],
        treatment: [
            '发病初期用代森锰锌、百菌清喷雾',
            '每7-10天1次，连续2-3次'
        ],
        images: []
    },
    {
        id: 'strawberry_leaf_scorch',
        name: '草莓叶枯病',
        category: '真菌病害',
        icon: '🍓',
        description: '又称"蛇眼病"，主要危害叶片。病斑多时叶片枯死，影响植株生长和花芽分化。',
        severity: '中风险',
        severityLevel: 'medium',
        symptoms: [
            '叶片出现紫红色小斑点',
            '扩大后中心变为灰白色，边缘紫红色',
            '病斑呈"蛇眼"状',
            '严重时病斑汇合，叶片枯死'
        ],
        causes: [
            '春秋季低温多雨易发病',
            '苗期和收获后最易感病',
            '连作障碍，土壤带菌'
        ],
        prevention: [
            '清理病叶，减少菌源',
            '控制氮肥，防止徒长',
            '合理密植，雨后及时排水'
        ],
        treatment: [
            '发病初期喷多菌灵、甲基托布津',
            '采收后彻底清园喷药'
        ],
        images: []
    },
    {
        id: 'rice_blast',
        name: '水稻稻瘟病',
        category: '真菌病害',
        icon: '🌾',
        description: '水稻三大病害之首，极具毁灭性。根据危害部位不同分为苗瘟、叶瘟、穗颈瘟等。',
        severity: '极高风险',
        severityLevel: 'high',
        symptoms: [
            '叶片出现梭形病斑，由褐点扩散',
            '病斑中心灰白色，边缘褐色（典型病斑）',
            '穗颈受害变褐枯死，造成白穗',
            '严重减产甚至绝收'
        ],
        causes: [
            '低温阴雨寡照天气',
            '偏施氮肥',
            '种植感病品种'
        ],
        prevention: [
            '选用抗病良种',
            '种子消毒处理',
            '科学管水，浅水勤灌，适时晒田'
        ],
        treatment: [
            '破口抽穗期是防治关键期',
            '喷施三环唑、稻瘟灵',
            '发现发病中心立即施药'
        ],
        images: []
    },
    {
        id: 'pepper_anthracnose',
        name: '辣椒炭疽病',
        category: '真菌病害',
        icon: '🌶️',
        description: '主要危害果实，引起果实腐烂，严重影响辣椒品质和产量。',
        severity: '中风险',
        severityLevel: 'medium',
        symptoms: [
            '果实出现水渍状黄褐色圆斑',
            '病斑凹陷，呈同心轮纹状排列黑色小点',
            '潮湿时溢出粉红色粘稠物',
            '病果易脱落或干缩'
        ],
        causes: [
            '高温高湿环境',
            '排水不良，种植过密',
            '日灼果易诱发此病'
        ],
        prevention: [
            '实行3年以上轮作',
            '加强田间管理，防涝排渍',
            '防止日灼，果实适当遮阴'
        ],
        treatment: [
            '发病初期喷施咪鲜胺、苯醚甲环唑',
            '雨前雨后及时用药'
        ],
        images: []
    }
]

export const classMap: Record<string, string> = {
    'Apple___Apple_scab': '苹果黑星病',
    'Apple___Black_rot': '苹果黑腐病',
    'Apple___Cedar_apple_rust': '苹果赤星病',
    'Apple___healthy': '苹果健康',
    'Blueberry___healthy': '蓝莓健康',
    'Cherry_(including_sour)___Powdery_mildew': '樱桃白粉病',
    'Cherry_(including_sour)___healthy': '樱桃健康',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': '玉米灰斑病',
    'Corn_(maize)___Common_rust_': '玉米普通锈病',
    'Corn_(maize)___Northern_Leaf_Blight': '玉米大斑病',
    'Corn_(maize)___healthy': '玉米健康',
    'Grape___Black_rot': '葡萄黑腐病',
    'Grape___Esca_(Black_Measles)': '葡萄黑麻疹',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': '葡萄褐斑病',
    'Grape___healthy': '葡萄健康',
    'Orange___Haunglongbing_(Citrus_greening)': '柑橘黄龙病',
    'Peach___Bacterial_spot': '桃细菌性穿孔病',
    'Peach___healthy': '桃健康',
    'Pepper,_bell___Bacterial_spot': '辣椒细菌性斑点病',
    'Pepper,_bell___healthy': '辣椒健康',
    'Potato___Early_blight': '马铃薯早疫病',
    'Potato___Late_blight': '马铃薯晚疫病',
    'Potato___healthy': '马铃薯健康',
    'Raspberry___healthy': '树莓健康',
    'Soybean___healthy': '大豆健康',
    'Squash___Powdery_mildew': '南瓜白粉病',
    'Strawberry___Leaf_scorch': '草莓叶枯病',
    'Strawberry___healthy': '草莓健康',
    'Tomato___Bacterial_spot': '番茄细菌性斑点病',
    'Tomato___Early_blight': '番茄早疫病',
    'Tomato___Late_blight': '番茄晚疫病',
    'Tomato___Leaf_Mold': '番茄叶霉病',
    'Tomato___Septoria_leaf_spot': '番茄斑枯病',
    'Tomato___Spider_mites Two-spotted_spider_mite': '番茄红蜘蛛',
    'Tomato___Target_Spot': '番茄靶斑病',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': '番茄黄化曲叶病毒病',
    'Tomato___Tomato_mosaic_virus': '番茄花叶病毒病',
    'Tomato___healthy': '番茄健康'
};

export const getChineseName = (className: string) => {
    return classMap[className] || className.replace(/___/g, ' - ').replace(/_/g, ' ');
};
