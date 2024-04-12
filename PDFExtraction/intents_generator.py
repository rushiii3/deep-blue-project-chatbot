import numpy as np
import nltk as nlp

class SubjectiveTest:

    def __init__(self, data):
        self.question_pattern = [
            "Explain the significance of ",
    "Discuss the financial implications of ",
    "Describe the key metrics related to ",
    "Analyze the trends in ",
    "Evaluate the financial performance of ",
    "Explain the impact of ",
    "Illustrate the concept of ",
    "Explain the relationship between ",
    "Evaluate the risk factors associated with ",
    "Discuss the financial strategy for ",
    "Elaborate on the financial forecast for ",
    "Explain the financial position of ",
    "Analyze the profitability of ",
    "Discuss the liquidity of ",
    "Evaluate the solvency of ",
    "Explain the efficiency of ",
    "Analyze the investment opportunities in ",
    "Discuss the cash flow of ",
    "Evaluate the return on investment for ",
    "Explain the concept of financial ratio analysis for ",
    "Discuss the financial health of ",
    "Evaluate the financial stability of ",
    "Describe the capital structure of ",
    "Analyze the performance indicators for ",
    "Discuss the budgeting process for ",
    "Explain the concept of financial modeling for ",
    "Evaluate the financial risk management of ",
    "Discuss the regulatory compliance of ",
    "Analyze the market position of ",
        ]

        self.grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
            {<NN>+<IN|DT>*<NNP>+}
            {<NNP>+<NNS>*}
        """
        self.summary = data
    
    @staticmethod
    def word_tokenizer(sequence):
        word_tokens = list()
        for sent in nlp.sent_tokenize(sequence):
            for w in nlp.word_tokenize(sent):
                word_tokens.append(w)
        return word_tokens
    
    def create_vector(answer_tokens, tokens):
        return np.array([1 if tok in answer_tokens else 0 for tok in tokens])
    
    def cosine_similarity_score(vector1, vector2):
        def vector_value(vector):
            return np.sqrt(np.sum(np.square(vector)))
        v1 = vector_value(vector1)
        v2 = vector_value(vector2)
        v1_v2 = np.dot(vector1, vector2)
        return (v1_v2 / (v1 * v2)) * 100
    
    # def generate_test(self):
    #     sentences = nlp.sent_tokenize(self.summary)
    #     cp = nlp.RegexpParser(self.grammar)
    #     question_answer_dict = dict()
    #     for sentence in sentences:
    #         tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
    #         tree = cp.parse(tagged_words)
    #         for subtree in tree.subtrees():
    #             if subtree.label() == "CHUNK":
    #                 temp = ""
    #                 for sub in subtree:
    #                     temp += sub[0]
    #                     temp += " "
    #                 temp = temp.strip()
    #                 temp = temp.upper()
    #                 if temp not in question_answer_dict:
    #                     question_answer_dict[temp] = sentence
    #                 else:
    #                     question_answer_dict[temp] += sentence
    #     keyword_list = list(question_answer_dict.keys())
    #     question_answer = list()
    #     while len(question_answer) < int(self.noOfQues):
    #         rand_num = np.random.randint(0, len(keyword_list))
    #         selected_key = keyword_list[rand_num]
    #         answer = question_answer_dict[selected_key]
    #         rand_num %= 4
    #         question = self.question_pattern[rand_num] + selected_key + "."
    #         print(selected_key)
    #         question_answer.append({"Question": question, "Answer": answer, "keyword":selected_key});
    #     que = [qa["Question"] for qa in question_answer]
    #     ans = [qa["Answer"] for qa in question_answer]
    #     key = [qa["keyword"] for qa in question_answer]
    #     return que, ans, key

    # def generate_test(self):
    #     sentences = nlp.sent_tokenize(self.summary)
    #     cp = nlp.RegexpParser(self.grammar)
    #     question_answer_dict = dict()
    #     generated_questions = set()  # To keep track of generated questions
    #     for sentence in sentences:
    #         tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
    #         tree = cp.parse(tagged_words)
    #         for subtree in tree.subtrees():
    #             if subtree.label() == "CHUNK":
    #                 temp = ""
    #                 for sub in subtree:
    #                     temp += sub[0]
    #                     temp += " "
    #                 temp = temp.strip()
    #                 temp = temp.upper()
    #                 if temp not in question_answer_dict:
    #                     question_answer_dict[temp] = sentence
    #                 else:
    #                     question_answer_dict[temp] += sentence
    #     keyword_list = list(question_answer_dict.keys())
    #     question_answer = list()
    #     while len(question_answer) < int(self.noOfQues):
    #         rand_num = np.random.randint(0, len(keyword_list))
    #         selected_key = keyword_list[rand_num]
    #         # Check if the selected question is already generated
    #         if selected_key not in generated_questions:
    #             answer = question_answer_dict[selected_key]
    #             rand_num %= 4
    #             question = self.question_pattern[rand_num] + selected_key + "."
    #             # Append the question along with the keyword
    #             question_answer.append({"Question": question, "Answer": answer, "Keyword": selected_key})
    #             # Add the selected question to the generated questions set
    #             generated_questions.add(selected_key)
    #     que = [qa["Question"] for qa in question_answer]
    #     ans = [qa["Answer"] for qa in question_answer]
    #     keys = [qa["Keyword"] for qa in question_answer]
    #     return que, ans, keys

    def generate_test(self):
        sentences = nlp.sent_tokenize(self.summary)
        cp = nlp.RegexpParser(self.grammar)
        question_answer_dict = dict()
        generated_questions = set()  # To keep track of generated questions
        for sentence in sentences:
            tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
            tree = cp.parse(tagged_words)
            for subtree in tree.subtrees():
                if subtree.label() == "CHUNK":
                    temp = ""
                    for sub in subtree:
                        temp += sub[0]
                        temp += " "
                    temp = temp.strip()
                    temp = temp.upper()
                    if temp not in question_answer_dict:
                        question_answer_dict[temp] = sentence
                    else:
                        question_answer_dict[temp] += sentence
        keyword_list = list(question_answer_dict.keys())
        if not keyword_list:  # Check if keyword_list is empty
            print("No keywords found in the question-answer dictionary. Skipping...")
            return None  # or any other value that indicates no keywords were found
        print(keyword_list)
        question_answer = list()
        while True:
            rand_num = np.random.randint(0, len(keyword_list))
            selected_key = keyword_list[rand_num]
            # Check if the selected question is already generated
            if selected_key not in generated_questions:
                answer = question_answer_dict[selected_key]
                rand_num %= 4
                question = self.question_pattern[rand_num] + selected_key + "."
                # Append the question along with the keyword
                question_answer.append({"Question": question, "Answer": answer, "Keyword": selected_key})
                # Add the selected question to the generated questions set
                generated_questions.add(selected_key)
            # Break the loop if all unique questions are generated
            if len(generated_questions) == len(keyword_list):
                break
        que = [qa["Question"] for qa in question_answer]
        ans = [qa["Answer"] for qa in question_answer]
        keys = [qa["Keyword"] for qa in question_answer]
        return que, ans, keys

# Example usage:
financial_data = ''' We have invested significant resources into research and development of our DFI system and Exensio platform and if we fail to successfully carry out these initiatives on the expected timeline or at all, our business, financial condition, or results of operations could be adversely impacted. As part of the evolution of our business, we have made substantial investments in research and development efforts to develop our DFI system and Exensio cloud-based platform. New competitors, technological advances in the semiconductor industry or by competitorsor other competitive factors may require us to further invest significantly greater resources than we anticipate. If we are required to invest significantly greater resources than anticipated without a corresponding increase in revenue, our operating results could decline. There can be no guarantee that the technologies or products that we invest in will result in products that create additional revenue. We may not recoup our research and development investments, which could cause our results to suffer. If our DFI system and Exensio platform do not anticipate technological changes in our industry or fail to meet market demand, we may not capture the market share we anticipate, lose our competitive position, our products may become obsolete, and our business, financial condition or results of operations could be adversely affected. Additionally, our periodic research and development expenses may be independent of our level of revenue, which could negatively impact our financial results. Our sales cycle is lengthy and customers may delay entering into contracts or decide not to adopt our products or solutions after we have performed services or supported their evaluation of our technology, which could result in delays in recognizing revenue and could negatively impact our results of operations in a quarter or result in lower revenue than we expected if a contract is not consummated. On-going negotiations and evaluation projects for new products, with new customers or in new markets may not result in significant revenues for us if we are unable to close new engagements on terms favorable to us, in a timely manner, or at all. Unexpected delays in our sales cycle could cause our revenues to fall short of expectations. Further, the timing and length of negotiations required to enter into agreements with our customers and the enforcement of our complex contractual provisions is difficult to predict. If we do not successfully negotiate certain key complex contractual provisions, if there are disputes regarding such provisions, or if they are not enforceable as we intended, our revenues and results of operations would suffer. Further, our customers sometimes delay starting negotiations until they begin developing a new process, have a need for a new product, or experience specific yield issues. This means that, on occasion we have, and may continue to provide technology and services under preliminary documentation before executing the final contract. In these cases, we would not recognize revenue and may defer associated costs until execution of a final contract, which, if significant, could negatively impact our results of operations in the periods before we execute a final contract. Further, if we were to incur significant costs and then fail to enter into a final contract, we would have to write-off such deferred costs in the period in which the negotiations ended, which would increase our costs and expenses and could result in significant operating losses. Our fixed-fee services or product or system installations/configurations may take longer than budgeted, which could slow our revenue recognition and may also result in a lost contract or a claim of breach by our customers, which would negatively affect our operating results. Our fixed-fee services, including for characterization, require a team of engineers to collaborate with our customers to address complex issues by using our software and other technologies, and the installation and configuration of our software into our customers\u2019 fabrication and test/assembly facilities requires experienced engineers working with our customers on active foundry and test/assembly equipment. We must accurately estimate the amount of resources needed to complete these types of services to determine when the engineers will be able to commence their next engagement. In addition, our accounting for contracts with such services, which generate fixed fees, sometimes requires adjustments to profit and loss based on revised estimates during the performance of the contract. These adjustments may have a material effect on our results of operations in the period in which they are made. The estimates giving rise to these risks, which are inherent in fixed-price contracts, include the forecasting of costs and schedules, and contract revenues related to contract 16 performance. If we fail to meet a customer\u2019s expectations in either case, the customer could claim that we breached our obligations, which could result in lost revenue and increased expenses. Our ability to sell our products, systems, and solutions depends in part on the quality of our support and services offerings, and the failure to offer high-quality support and services could negatively affect our sales and results of operations. Once our products are integrated within our customers\u2019 hardware and software systems, our customers may depend on our support organization to resolve any issues relating to our products. Further, in connection with delivering our SaaS, which requires us to maintain adequate server hardware and internet infrastructure, including system redundancies, we are required to meet contractual uptime obligations. A high level of system and support is critical for the successful marketing and sale of our products. If we do not effectively provide subscription access to our SaaS customers, assist our customers in deploying our products, succeed in helping our customers quickly resolve post- deployment issues, and provide effective on-going support and the privacy and data security capabilities required by our customers, we may face contractual penalties or customers may not renew subscriptions or services in the future, which would negatively impact our results of operations. In addition, due to our international operations, our system and support organization faces challenges associated with delivering support, hours that support is available, training, and documentation where the user\u2019s native language may not be English. If we fail to maintain high-quality support and services or fail to adequately address our customers\u2019 support needs, our customers may choose our competitors\u2019 products instead of ours in the future, which would negatively affect our revenues and results of operations. Defects in our proprietary technologies, hardware and software tools, and failure to effectively remedy any such defects could decrease our revenue and our competitive market share. If the software, hardware, or proprietary technologies we provide to customers contain defects that negatively impact customers\u2019 ability to use our systems or software, increase our customers\u2019 cost of goods sold or time-to-market, or damage our customers\u2019 property, such defects could significantly decrease the market acceptance of our products and services or could result in warranty or other claims. We must adequately train our new personnel, especially our customer service and technical support personnel, to effectively and accurately, respond to and support our customers. If we fail to do this, it could lead to dissatisfaction among our customers, which could slow our growth. Further, the cost of support resources required to remedy any defects in our technologies, hardware, or software tools could exceed our expectations. Any actual or perceived defects with our software, hardware, or proprietary technologies may also hinder our ability to attract or retain industry partners or customers, leading to a decrease in our revenue. These defects are frequently found during the period following introduction of new software, hardware, or proprietary technologies or enhancements to existing software, hardware, or proprietary technologies, which means that we may not discover the errors or defects until after customer implementation. If our software, hardware, or proprietary technologies contain errors or defects, it could require us to expend significant resources to remedy these problems or defend/ indemnify claims, which could reduce margins and result in the diversion of technical and other resources from our other customer implementations and development efforts. Objectionable disclosure of our customers\u2019 confidential information or our failure to comply with our customers\u2019 security rules, including for those related to SaaS access or our on-site access could result in costly litigation, cause us to lose existing and potential customers, or negatively impact on-going business with existing customers. Our customers consider their product yield and test information and other confidential information, which we collect in the ordinary course of our engagement with the customer or through our software tools, including data and personal data about our customers\u2019 employees necessary to administer the licenses, to be extremely competitively sensitive or subject to strict protection frameworks. Many of our customers have strict security rules for on-site access to, hosting of, or transfer of their confidential information. As a result of increased regulatory and customer scrutiny of all data processing activities, as well as increasing and evolving regulation of such practices, we have security obligations on how we collect, transfer and use data (including personal data), which could require us to expend money and resources to comply with those requirements, and if compromised, could have a material adverse effect on our business, financial condition and results of operations, including the potential for regulatory investigations, enforcement actions, lawsuits and a loss of business and a degradation of our reputation. If we suffer an unauthorized intrusion or we inadvertently disclose or are required to disclose this information, or disclose this information in a manner that was objectionable to our customers, 17 regulators, consumer protection groups, or privacy groups, or if we fail to adequately comply with customers\u2019 security protocols for accessing or hosting confidential information, our reputation could be materially adversely affected, we could lose existing and potential customers or could be subject to costly penalties or litigation, or our on-going business could be negatively impacted and insurance to cover such situations may not fully cover our exposure. If we fail to implement industry standard protections and processing procedures, the growing awareness of our customers and potential customers regarding privacy and data security requirements and/or adverse media coverage or regulatory scrutiny could limit the use and adoption of our services. In addition, to avoid potential disclosure of confidential information to competitors, some of our customers may, in the future, ask us not to work with key products or processes, which could limit our revenue opportunities. We generate a significant portion of our revenues from a limited number of customers, and a large percentage of our revenues from two customers, so defaults or decreased business with, or the loss of, any one of these customers, or pricing pressure, or customer consolidation could significantly reduce our revenues or margins and negatively impact results of operations. Historically, we have had a small number of large customers that contribute significant revenues. In the year ended December 31, 2022, two customers accounted for 41% of our total revenues. We have in the past and could in the future lose a customer due to its decision not to develop or produce its own future process node or not to engage us on future process nodes. We could also lose customers as a result of industry factors, including but not limited to reduced manufacturing volume or consolidation. Consolidation among our customers could also lead to increased customer bargaining power, or reduced customer spending on software and services. Further, new business may be delayed if a key customer uses its leverage to push for terms that are worse for us and we delay entering into the contract to negotiate for better terms, in which case revenue in any particular quarter or year may fail to meet expectations. Also, the loss of any of these customers or the failure to secure new contracts with these customers could further increase our reliance on our remaining customers. Further, if any of our key customers default, declare bankruptcy or otherwise delay or fail to pay amounts owed, or we otherwise have a dispute with any of these customers, our results of operations would be negatively affected in the short term and possibly the long term. For example, in 2022, 2021 and 2020 we incurred expenses in the amount of $1.9 million, $2.0 million and $1.1 million, respectively, related to the arbitration with SMIC New Technology Research & Development (Shanghai) Corporation due to SMIC\u2019s failure to pay fees due to us under a series of contracts. In early 2023, we will incur substantial additional expenses related to an arbitration hearing to resolve this matter. The loss of revenue from any of our key customers would cause significant fluctuations in results of operations because our expenses are fixed in the short term and it takes us a long time to replace customers or reassign resources. If we do not continuously meet our development milestones of key research and development projects or successfully commercialize our Design-for-Inspection system, our future market opportunity and revenues will suffer, and our costs may not be recouped. We have invested significantly in the design and development of our eProbe tool and related IP. Key customers failing to purchase, renew, or expand the number or use of such systems on our expected timeline or at all will cause our results to miss expectations. Also, if the results of our DFI system, including new applications, are not as we expect, we may not be able to successfully commercialize this system or such applications on schedule, or at all, and we may miss the market opportunity and not recoup our investment. Further, our eProbe tool could cause unexpected damage to wafers or delay processing wafers, which we could be liable for, or which could make customers unwilling to use it. If we are not able to create significant interest and show reliable and useful results without significant damage to wafers, our investment may not be recouped and our future results may suffer. We are required to comply with governmental export and import requirements that could subject us to liability and restrict our ability to sell our products and services, which could impair our ability to compete in international markets. We are required to comply with export controls and economic sanctions laws and regulations that restrict selling, shipping or transmitting our products and services and transferring our technology outside the United States. These 18 requirements also restrict domestic release of software and technology to foreign nationals. In addition, we are subject to customs and other import requirements that regulate imports that are important for our business. If we fail to comply with the U.S. Export Administration Regulations or other U.S. or non-U.S. export or economic sanctions laws and regulations (collectively, \u201cExport Regulations\u201d), we could be subject to substantial civil and criminal penalties, including fines for the Company and the possible loss of the ability to engage in exporting and other international transactions. Due to the nature of our business and technology, Export Regulations may also subject us to governmental inquiries regarding transactions between us and certain foreign entities. Export Regulations are fluid, complex, and uncertain, and there are ongoing efforts throughout the industry in coordination with regulators to revise, clarify, and interpret Export Regulations. The U.S. Congress and regulators continue to consider significant changes in laws and regulations. We cannot predict the impact that additional legal changes may have on our business in the future. For example, in October 2022 the U.S. Bureau of Industry and Security (\u201cBIS\u201d) promulgated broad, novel Export Regulations relating to China that temporarily caused us to pause some deliveries while we interpreted the application of the new regulations on our business, given current and evolving operations.  Also, BIS has placed certain entities on its entity list (the \u201cEntity List\u201d), which restricts supply of items to or in connection with the named entities. Further, in some circumstances Export Regulations require a license to export an item if the recipient will use the item to design or produce an item for a Huawei-affiliated company or certain other organizations on the Entity List. These regulations can also require licenses for exports that involve Chinese military or intelligence-related end users or end uses. Future changes in Export Regulations, including changes in the enforcement and scope of such regulations, may create delays in the introduction of our products or services in international markets or could prevent our customers with international operations from deploying our products or services globally. In some cases, such changes could prevent the export of our products or services to certain countries, governments, entities or individuals altogether. Any such delays or restrictions could adversely affect our business, financial condition and results of operations. For further discussion, see Item 7. \u201cManagement\u2019s Discussion and Analysis of Financial Condition and Results of Operations.\u201d Decreases in wafer volumes at our customers\u2019 manufacturing sites or the volume of ICs that some of our customers are able to sell to their customers would cause our Integrated Yield Ramp revenue to suffer. Our Integrated Yield Ramp revenue includes amounts largely determined by variable wafer volumes at manufacturing sites covered by our contracts and, in some cases, determined by the volume of an IC product that our customer is able to sell to its customers. Both of these factors are outside of our control. We have seen a significant reduction in our Integrated Yield Ramp revenue in recent years and expect this trend to continue. Further, some of our manufacturing customers\u2019 business is largely dependent on customers that use our manufacturing customer as a second or third source. If those customers consolidate and/or otherwise move the orders to manufacturing facilities not covered by our contracts, or suspend their manufacturing at covered facilities for any reason, including consolidation, our Integrated Yield Ramp revenue will continue to decrease, which could negatively affect our financial results. Further, reduced demand for semiconductor products or protectionist policies like those stemming from the complex relationships among China, Hong Kong, Taiwan, and the United States has from time to time decreased and may continue to decrease the volume of wafers and, in some cases, products our customers are able to make or sell, which would also decrease our Integrated Yield Ramp revenue. Also, our customers may unilaterally decide to implement changes to their manufacturing processes during the period that volume is covered by royalty contracts, which could negatively affect yield results and, thus, our Integrated Yield Ramp revenue. Since we currently work on a small number of large projects at specified manufacturing sites and, in some cases, on specific IC products, our results of operations have been and may continue to be adversely affected by negative changes at those sites or in those products, including slowdowns in manufacturing due to external factors, such as U.S. trade restrictions, rising inflation and global interest rates, the impact of the on-going COVID-19 pandemic, or continued or worsening supply chain disruptions. Also, if wafer orders from sites covered by our contracts are not secured by our customers, if an end product does not achieve commercial viability, if a process line or, in some cases, a specific product, does not achieve significant increases in yield or sustain significant volume manufacturing during the time we receive royalties, revenues associated with such volumes or products would be negatively impacted. This could significantly reduce our Integrated Yield Ramp revenue and our results of operations could fail to meet expectations. In addition, if we 19 work with two directly competitive manufacturing facilities or products, volume in one may offset volume, and thus any of our related revenue, in the other facility or product. Our success depends upon our ability to effectively plan and manage our resources and restructure our business through rapidly fluctuating economic and market conditions, which actions may have an adverse effect on our financial and operating results. Our ability to successfully offer our products and services in a rapidly evolving market requires an effective planning, forecasting, and management process to enable us to effectively scale and adjust our business and business models in response to fluctuating market opportunities and conditions, which has and could continue to require us to increase headcount, acquire new companies or engage in restructurings from time to time. For example, while we have increased investment in our business by increasing headcount, acquiring companies, and increasing our investment in R&D, sales and marketing, and other parts of our business from time to time, at other times we have undertaken restructuring  initiatives to reduce expenses and align our operations with evolving business needs. Some of our expenses related to such efforts are fixed costs that cannot be rapidly or easily adjusted in response to fluctuations in our business or headcount. Rapid changes in the size, alignment or organization of our workforce, including sales account coverage, could adversely affect our ability to develop and deliver products and services as planned or impair our ability to realize our current or future business and financial objectives. Our ability to achieve the anticipated cost savings and other benefits from restructuring initiatives within the expected time frame is subject to many estimates and assumptions, which are subject to significant economic, competitive and other uncertainties, some of which are beyond our control. If these estimates and assumptions are incorrect, if we are unsuccessful at implementing changes, or if other unforeseen events occur, our business and results of operations could be adversely affected Our business may be impacted by geopolitical events and uncertainties, war, terrorism, or other business interruptions beyond our control. Geopolitical uncertainties, including relations between the United States and each of China and Russia, war, terrorism, or other business interruptions could cause damage to, disrupt, or cancel sales of our products and services on a global or regional basis, which could have a material adverse effect on our business or vendors with which we do business. Due to the significance of our China market for our profit and growth, we are exposed to risks in China, including the risks mentioned elsewhere and the following: the effects of current U.S.-China relations, including rounds of tariff increases and retaliations and increasing restrictive regulations, potential boycotts and increasing anti-Americanism; escalating U.S.- China tension and increasing political sensitivities in China; and unexpected governmental regulations and restrictions in China as a result of renewed or increased efforts to contain the COVID-19 pandemic, which could negatively impact our local operations. Such events could also make it difficult or impossible for us to deliver products and services to our customers. In addition, territorial invasions can lead to cybersecurity attacks on technology companies, such as ours, located far outside of the conflict zone. In the event of prolonged business interruptions or negative broad economic and security conditions due to geopolitical events, we could incur significant losses, require substantial recovery time, and experience significant expenditures in order to resume our business operations. In addition, our insurance policies typically contain a war exclusion of some description and we do not know how our insurers are likely to respond in the event of a loss alleged to have been caused by geopolitical uncertainties. Global economic conditions or semiconductor market conditions could materially adversely impact demand for our products and services, decrease our sales, or delay our sales cycle. Our customers are global semiconductor companies, which means that our operations and performance depend significantly on worldwide economic conditions as well as semiconductor market specific changes. Uncertainty about global economic conditions including war, terrorism, geopolitical uncertainties and other business interruptions could result in damage to, disruption, postponement or cancellation of sales of our products or services on a global or regional basis. Furthermore, tighter credit, higher interest rates, inflationary concerns, unemployment, negative financial news and/or declines in income or asset values and other macroeconomic factors could have a material adverse effect on demand for our products and services and, accordingly, on our business, results of operations or financial condition and/or vendors with which we do business. For example, the timing of the build-out of the semiconductor market in China depends significantly on governmental funding on both local and national levels and a delay in this funding could negatively affect 20 our revenues. Further, any economic and political uncertainty caused by the United States tariffs imposed on goods from China or enhanced U.S. export regulations relating to China, among other potential countries, and any corresponding tariffs from China or such other countries in response, may negatively impact demand and/or increase the cost for our products. Similarly, the on-going COVID-19 pandemic in China or in other nations has and may continue to cause a slowdown in the global economy and demand for our products and services. Further, the semiconductor industry historically has been volatile with up cycles and down cycles, due to sudden changes in customers\u2019 manufacturing capacity requirements and spending, which depend in part on capacity utilization, demand for customers\u2019 IC products by consumers, inventory levels relative to demand, and access to affordable capital. As a result of the various factors that affect this volatility, the timing and length of any cycles can be difficult to predict and could be longer than anticipated. Any of these events could negatively affect our revenues and make it challenging or impossible for us to deliver products and services to our customers forecast our operating results, make business decisions, and identify the risks that may affect our business, financial condition and results of operations. Customers with liquidity issues may also lead to additional bad debt expense. Supply-chain disruptions could impact our ability to build additional hardware tools or meet customer deadlines. Disruptions to our supply chain may significantly increase our component costs and could impact our ability to build additional hardware tools, which would decrease our sales, earnings, and liquidity or otherwise adversely affect our business and result in increased costs. Such a disruption could occur as a result of any number of events, including, but not limited to: rising inflation and global interest rates increasing component costs, a closure or slowdown at our suppliers\u2019 plants or shipping delays including, for example, those made to combat the spread of COVID-19, market shortages for critical components, increases in prices, the imposition of regulations, quotas, embargoes or tariffs on components or our products, labor stoppages or shortages, supply chain disruptions, third-party interference, cyberattacks, severe weather conditions including the adverse effects of climate change-related events, geopolitical developments, war or terrorism, and disruptions in utilities and other services. In addition, the development, licensing, or acquisition of new products in the future may increase the complexity of supply chain management. Failure to effectively manage our supply of components and products could adversely affect our business.'''
# test_generator = SubjectiveTest(financial_data)
# questions, answers, keywords = test_generator.generate_test()
# for q, a, k in zip(questions, answers,keywords):
#     print("Question:", q)
#     print("Answer:", a)
#     print("Keywords:",k)
#     print()
