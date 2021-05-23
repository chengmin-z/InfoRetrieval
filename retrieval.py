def retrieval_query(input_str: str):
    result = mock_example_query(input_str)
    return result


def mock_example_query(input_str: str):
    input_str_keywords = ['丁香', '马来西亚']
    result_1 = {
        'name': '丁香',
        'url': 'http://www.zhongyoo.com/name/dingxiang_39.html',
        'img_url': 'http://www.zhongyoo.com/uploads/allimg/130530/1-13053015424DE.jpg',
        'contained_keywords': ['丁香', '马拉西亚'],
        'query_match': 1.0,
        'content':
        '''【中药名】丁香 dīngxiāng
【别名】丁子香、支解香、公丁香。
【英文名】Flos Caryophylli
【药用部位】桃金娘科植物丁香Eugenia caryophyllata Thunb.的花蕾。
【植物形态】多年生常绿乔木，高12米。树皮灰白色而光滑。单叶对生，革质，卵状长椭圆形至披针形，先端尖，基部狭呈楔形，全缘，侧脉多，平行状，具多数透明小油点，叶柄明显。花顶生，3朵一组，集成聚伞形圆锥花序；花萼筒状，顶端4裂，裂片呈三角形，肉质肥厚，有油腺；花冠圆头状，花瓣4，白色而现微紫色；雄蕊多数，子房下位，柱头细小。浆果红色或深紫色，卵圆形，内有种子1粒，呈椭圆形。
【产地分布】原产于马来西亚、印度尼西亚及东非沿岸国家，现我国有栽培。
【采收加工】当花蕾由绿色转红时采摘，晒干。
【药材性状】略研棒状。花冠圆球形，花瓣4，覆瓦状抱合，棕褐色至黄褐色，花瓣内为雄蕊和花柱，搓碎后可见众多黄色细粒状的花药。萼筒圆柱状，略扁，有的稍弯曲，红棕色或棕褐色，上部有4枚三角状的萼片，&ldquo;十&rdquo;字形分开。质坚实，富油性。气芳香浓烈，味辛辣，有麻舌感。
【性味归经】味辛，性温。归胃经、脾经、肾经。
【功效与作用】温中降逆、补肾助阳。属温里药。
【临床应用】用量1～3克，煎服。用治脾胃虚寒、呃逆呕吐、食少吐泻、心腹冷痛、肾虚阳痿。
【药理研究】抗胃溃疡，止泻，利胆，镇痛，抗缺氧，抗凝血，抗突变，抑菌杀虫。具健胃作用，浸出液具有明显的刺激胃液分泌作用，并能缓解腹胀、恶心、呕吐等。另外，对多种致病性真菌、球菌、链球菌及肺炎、痢疾、大肠、伤寒等杆菌以及流感病毒有抑制作用。
【化学成分】含挥发油15%～20%，油中主成分为丁香油酚、&beta;-丁香烯、乙酰基丁香油酚等。另含丁香酚、乙酰丁香酚、异槲皮素、山柰酚、槲皮素、石竹烯氧化物、齐墩果酸、&alpha;-衣兰油烯等成分。
【使用禁忌】热病及阴虚内热者忌服。
【配伍药方】①治朝食暮吐：丁香十五个。研末。甘蔗汁、姜汁和丸莲子大。噙咽之。(《摘玄方》)
②治久心痛不止：丁香15克，桂心30克。捣细，罗为散，每于食前，以热酒调下3克。(《圣惠方》)
③治冷心疼，面青唇黑，手足厥冷：丁香、良姜、官桂各4.5克。水一碗煎七分，用胡椒二十粒炒黄色为末，调入汤药内热服。(《心医集》)
④治妇人崩中，昼夜不止：丁香60克，酒二升，煎一升，分服。(《梅师方》)
⑤治乳头裂破：捣丁香末敷之。(《梅师方》)'''
    }
    return {
        'origin_input_str': input_str,
        'input_str_keywords': input_str_keywords,
        'results': [result_1, result_1]  # 数组
    }
