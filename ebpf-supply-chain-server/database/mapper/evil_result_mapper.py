from config.setting import db
import time


class EvilResult(db.Model):
    __tablename__ = 'supply_chain_evil_result'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hook_type = db.Column(db.String(255), nullable=True, default="pypi")
    hook_id = db.Column(db.BigInteger(), nullable=True, default=0)
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    rule_name = db.Column(db.Text, nullable=True, default="")
    score = db.Column(db.String(300), nullable=True, default="")
    hash = db.Column(db.String(300), nullable=True, default="")
    status = db.Column(db.Integer, nullable=True, default=0)
    create_time = db.Column(db.String(300), nullable=False)

    def insert(self, data: dict) -> int:
        mapper = EvilResult(hook_type=data.get("hook_type", ""),
                            rule_name=data.get("rule_name", ""),
                            hook_id=data.get("hook_id", 0),
                            package=data.get("package", ""),
                            version=data.get("version", ""),
                            describe=data.get("describe", ""), 
                            score=data.get("score", ""),
                            hash=data.get("hash", ""),
                            create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id
    
    def query_count_by_hash(self, hash: str) -> int:
        total = db.session.query(EvilResult).filter(EvilResult.hash==hash).count()
        db.session.close()
        return total
