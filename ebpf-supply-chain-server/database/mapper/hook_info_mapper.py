from config.setting import db
import time


class HookInfoSocket(db.Model):
    __tablename__ = 'supply_chain_hook_info_socket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, default="pypi")
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    comm = db.Column(db.String(300), nullable=True, default="")
    d_addr = db.Column(db.String(300), nullable=True, default="")
    d_port = db.Column(db.Integer, nullable=True, default=0)
    create_time = db.Column(db.BigInteger(), nullable=False)

    def insert(self, data: dict) -> int:
        mapper = HookInfoSocket(type=data.get("type", ""), package=data.get("package", ""),
                                version=data.get("version", ""),
                                describe=data.get("describe", ""),
                                comm=data.get("comm", "").replace("\u0000", ""), d_addr=data.get("daddr", ""),
                                d_port=data.get("dport", 0),
                                create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id

    def query_id_by_hook_info(self, package: str, version: str, d_addr: str, d_port: int) -> int:
        mapper = db.session.query(HookInfoSocket).filter(HookInfoSocket.package==package,
                                                        HookInfoSocket.version==version,
                                                        HookInfoSocket.d_addr==d_addr,
                                                        HookInfoSocket.d_port==d_port).first()
        db.session.close()
        if mapper is None:
            return None
        return mapper.id

    def query_count_by_addr(self, d_addr: str) -> int:
        total = db.session.query(HookInfoSocket).filter(HookInfoSocket.d_addr==d_addr).count()
        db.session.close()
        return total


class HookInfoSysOpen(db.Model):
    __tablename__ = 'supply_chain_hook_info_sys_open'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, default="pypi")
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    comm = db.Column(db.String(300), nullable=True, default="")
    pid = db.Column(db.BigInteger(), nullable=True, default=0)
    filename = db.Column(db.String(300), nullable=True, default="")
    create_time = db.Column(db.BigInteger(), nullable=False)

    def insert(self, data: dict):
        mapper = HookInfoSysOpen(type=data.get("type", ""), package=data.get("package", ""),
                                 version=data.get("version", ""),
                                 describe=data.get("describe", ""),
                                 comm=data.get("comm", ""),
                                 pid=data.get("pid", 0),
                                 filename=data.get("filename", "").replace("\u0000", ""),
                                 create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id


class HookInfoSysWrite(db.Model):
    __tablename__ = 'supply_chain_hook_info_sys_write'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, default="pypi")
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    comm = db.Column(db.String(300), nullable=True, default="")
    pid = db.Column(db.BigInteger(), nullable=True, default=0)
    filename = db.Column(db.String(300), nullable=True, default="")
    create_time = db.Column(db.BigInteger(), nullable=False)

    def insert(self, data: dict):
        mapper = HookInfoSysWrite(type=data.get("type", ""), package=data.get("package", ""),
                                 version=data.get("version", ""),
                                 describe=data.get("describe", ""),
                                 comm=data.get("comm", ""), 
                                 pid=data.get("pid", 0),
                                 filename=data.get("filename", "").replace("\u0000", ""),
                                 create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id


class HookInfoSysExec(db.Model):
    __tablename__ = 'supply_chain_hook_info_sys_exec'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, default="pypi")
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    comm = db.Column(db.String(300), nullable=True, default="")
    pid = db.Column(db.BigInteger(), nullable=True, default=0)
    filename = db.Column(db.String(300), nullable=True, default="")
    create_time = db.Column(db.BigInteger(), nullable=False)

    def insert(self, data: dict):
        mapper = HookInfoSysExec(type=data.get("type", ""), package=data.get("package", ""),
                                 version=data.get("version", ""),
                                 describe=data.get("describe", ""),
                                 comm=data.get("comm", ""), 
                                 pid=data.get("pid", 0),
                                 filename=data.get("filename", "").replace("\u0000", ""),
                                 create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id

    def query_id_by_hook_info(self, hook_info: dict) -> int:
        mapper = db.session.query(HookInfoSysExec).filter(HookInfoSysExec.package==hook_info.get("package", ""),
                                    HookInfoSysExec.version==hook_info.get("version", ""),
                                    HookInfoSysExec.comm==hook_info.get("comm", ""),
                                    HookInfoSysExec.pid==hook_info.get("pid", 0),
                                    HookInfoSysExec.filename==hook_info.get("filename", ""),
                                    HookInfoSysExec.create_time==hook_info.get("create_time", 0)
                                    ).first()
        db.session.close()
        if mapper is None:
            return None
        return mapper.id



class HookInfoDns(db.Model):
    __tablename__ = 'supply_chain_hook_info_dns'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=True, default="pypi")
    package = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(50), nullable=True, default="")
    describe = db.Column(db.Text, nullable=True, default="")
    comm = db.Column(db.String(300), nullable=True, default="")
    pid = db.Column(db.BigInteger(), nullable=True, default=0)
    host = db.Column(db.String(300), nullable=True, default="")
    create_time = db.Column(db.BigInteger(), nullable=False)

    def insert(self, data: dict):
        mapper = HookInfoDns(type=data.get("type", ""), package=data.get("package", ""),
                                 version=data.get("version", ""),
                                 describe=data.get("describe", ""),
                                 comm=data.get("comm", ""), 
                                 pid=data.get("pid", 0),
                                 host=data.get("host", ""),
                                 create_time=int(time.time()))
        db.session.add(mapper)
        db.session.flush()
        db.session.commit()
        id = mapper.id
        db.session.close()
        return id

    def query_id_by_hook_info(self, hook_info: dict) -> int:
        mapper = db.session.query(HookInfoDns).filter(HookInfoDns.package==hook_info.get("package", ""),
                                    HookInfoDns.version==hook_info.get("version", ""),
                                    HookInfoDns.comm==hook_info.get("comm", ""),
                                    HookInfoDns.pid==hook_info.get("pid", 0),
                                    HookInfoDns.host==hook_info.get("host", ""),
                                    HookInfoDns.create_time==hook_info.get("create_time", 0)
                                    ).first()
        db.session.close()
        if mapper is None:
            return None
        return mapper.id
