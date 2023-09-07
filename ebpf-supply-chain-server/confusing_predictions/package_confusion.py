from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from modules.logger import logger
from database.redis_db import Redis
from lxml import etree


class PypiConfusionPredictionsSvm(object):

    def __init__(self):
        super().__init__()
        self.compliant_samples = []
        self.confusing_samples = []
        self.redis = Redis()
        self.logger = logger
        self.tfidf_vectorizer = TfidfVectorizer()
        self.svm_classifier = SVC(kernel='linear', C=1.0, random_state=42)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PypiConfusionPredictionsSvm, cls).__new__(cls)
        return cls.instance

    def set_compliant_samples(self, simple_html: object) -> None:
        if simple_html is None:
            self.logger.error("simple_html is None")
            return
        self.compliant_samples = []
        root = etree.HTML(simple_html)
        nodes = root.xpath("//a")

        for node in nodes:
            self.compliant_samples.append(node.text)

    def set_confusing_samples(self) -> None:
        """
        获取黑名单、黑名单采集后维护在redis中，采集目前为手动采集
        """
        samples_cache_len = self.redis.llen("SKLEARN:CONFUSION:MALICIOUS")
        for length in range(1, int(samples_cache_len / 1000) + 1):
            cache_results = self.redis.lrange("SKLEARN:CONFUSION:MALICIOUS", (length - 1) * 1000, length * 100)
            self.confusing_samples = self.confusing_samples + cache_results

        for confusing in self.confusing_samples:
            self.compliant_samples.remove(confusing)

    def transform_svm(self) -> None:
        labels = [1] * len(self.compliant_samples) + [0] * len(self.confusing_samples)
        all_samples = self.compliant_samples + self.confusing_samples

        self.tfidf_vectorizer = TfidfVectorizer()
        x = self.tfidf_vectorizer.fit_transform(all_samples)
        x_train, x_test, y_train, y_test = train_test_split(x, labels, test_size=0.2, random_state=42)

        self.svm_classifier.fit(x_train, x_train)
        y_pred = self.svm_classifier.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        self.logger.info(f"transform_svm accuracy:{accuracy}")
        report = classification_report(y_test, y_pred, target_names=["Confusing", "Compliant"], zero_division=1)
        self.logger.info(f"transform_svm report:{report}")

    def prediction_with_svm(self, example: list) -> object:
        example_features = self.tfidf_vectorizer.transform(example)
        example_predictions = self.svm_classifier.predict(example_features)
        return zip(example, example_predictions)
