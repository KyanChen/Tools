# Readme.md
本脚本是为了根据iou来分辨正负样本和模糊样本，阈值设置pos_threshold, neg_threshold。    
主要是为了给SVM提供正负样本数据。   
输入输出均为TXT文档  
具体的，标签库为class left top right bottom shape为：n*5。  
待标记候选区域为(class) left top right bottom 其他特征。    
策略为：把候选区域每一个候选区域与标签库对应样本的标签进行iou计算，大于pos_threshold设置为正样本，小于neg_threshold为负。  
输出为：1或0 其他特征  
