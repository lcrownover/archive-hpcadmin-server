from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from . import models
from . import crud
import pytest


class TestDatabase:
    def setup_class(self):
        self.SQLALCHEMY_DATABASE_URL = "sqlite://"
        self.engine = create_engine(
            self.SQLALCHEMY_DATABASE_URL,
            connect_args={"check_same_thread": False},
            echo=True,
        )
        self.SessionLocal = sessionmaker(
            autoflush=False, autocommit=False, bind=self.engine
        )
        self.Base = declarative_base()
        self.db = self.SessionLocal()
        models.Base.metadata.create_all(bind=self.engine)

    def teardown_class(self):
        self.Base.metadata.drop_all(bind=self.engine)
        self.db.close()

    def test_get_users_none(self):
        from .crud import get_users

        users = get_users(self.db)
        assert len(users) == 0

    def test_create_user_timmy(self):
        from .crud import create_user
        from ..api import schemas

        s = schemas.UserCreate(
            username="timmyt",
            firstname="Timmy",
            lastname="Test",
            email="timmyt@gmail.com",
            is_pi=False,
            sponsor_id=None,
        )
        u = create_user(self.db, s)
        assert (
            u.username == "timmyt"
            and u.firstname == "Timmy"
            and u.lastname == "Test"
            and u.email == "timmyt@gmail.com"
            and u.is_pi == False
            and u.sponsor_id == None
        )

    def test_create_user_mike(self):
        from ..api import schemas
        from .crud import create_user

        # mike's ID should be 2
        s = schemas.UserCreate(
            username="mikem",
            firstname="Mike",
            lastname="Mock",
            email="mikem@gmail.com",
            is_pi=True,
            sponsor_id=None,
        )
        u = create_user(self.db, s)
        assert (
            u.username == "mikem"
            and u.firstname == "Mike"
            and u.lastname == "Mock"
            and u.email == "mikem@gmail.com"
            and u.is_pi == True
            and u.sponsor_id == None
        )

    def test_create_user_marie_sponsored_by_mike(self):
        from ..api import schemas
        from .crud import create_user

        # marie should be sponsored by mike
        s = schemas.UserCreate(
            username="mariem",
            firstname="Marie",
            lastname="Mock",
            email="mariem@gmail.com",
            is_pi=False,
            sponsor_id=2,
        )
        u = create_user(self.db, s)
        assert (
            u.username == "mariem"
            and u.firstname == "Marie"
            and u.lastname == "Mock"
            and u.email == "mariem@gmail.com"
            and u.is_pi == False
            and u.sponsor_id == 2
        )

    def test_create_user_duplicate(self):
        from ..api import schemas
        from .crud import create_user

        s = schemas.UserCreate(
            username="timmyt",
            firstname="Timmy",
            lastname="Test",
            email="timmyt@gmail.com",
            is_pi=False,
            sponsor_id=None,
        )
        with pytest.raises(crud.UserAlreadyExistsError):
            create_user(self.db, s)

    def test_get_users_length(self):
        from .crud import get_users

        users = get_users(self.db)
        assert len(users) == 3

    def test_get_user_timmy_id(self):
        from .crud import get_user

        u = get_user(self.db, 1)
        assert (
            u != None
            and u.username == "timmyt"
            and u.firstname == "Timmy"
            and u.lastname == "Test"
            and u.email == "timmyt@gmail.com"
        )

    def test_get_user_by_username(self):
        from .crud import get_user_by_username

        u = get_user_by_username(self.db, "timmyt")
        assert (
            u != None
            and u.username == "timmyt"
            and u.firstname == "Timmy"
            and u.lastname == "Test"
            and u.email == "timmyt@gmail.com"
        )

    def test_get_user_not_found(self):
        from .crud import get_user

        u = get_user(self.db, 4)
        assert u == None

    def test_get_pirgs_none(self):
        from .crud import get_pirgs

        pirgs = get_pirgs(self.db)
        assert len(pirgs) == 0

    def test_create_pirg_awesome(self):
        from ..api import schemas
        from .crud import create_pirg

        s = schemas.PirgCreate(name="awesome", owner_id=1, admin_ids=None, user_ids=[1])
        p = create_pirg(self.db, s)
        assert p != None and p.name == "awesome"

    def test_create_pirg_cool_with_admins(self):
        from ..api import schemas
        from .crud import create_pirg

        s = schemas.PirgCreate(name="cool", owner_id=1, admin_ids=[2], user_ids=[1, 2])
        p = create_pirg(self.db, s)
        assert (
            # users should be len 1 since userid1 is the owner
            p != None
            and p.name == "cool"
            and len(p.admins) == 1
            and len(p.users) == 1
        )

    def test_get_pirg_awesome(self):
        from .crud import get_pirg

        p = get_pirg(self.db, pirg_id=1)
        assert p != None and p.name == "awesome"

    def test_get_pirg_cool(self):
        from .crud import get_pirg

        p = get_pirg(self.db, pirg_id=2)
        assert p != None and p.name == "cool"

    def test_create_pirg_duplicate(self):
        from ..api import schemas
        from .crud import create_pirg

        s = schemas.PirgCreate(name="awesome", owner_id=1, admin_ids=None, user_ids=[1])
        with pytest.raises(crud.PirgAlreadyExistsError):
            create_pirg(self.db, s)

    def test_get_pirgs(self):
        from .crud import get_pirgs

        pirgs = get_pirgs(self.db)
        assert len(pirgs) == 2

    def test_get_pirg_awesome_id(self):
        from .crud import get_pirg

        p = get_pirg(self.db, pirg_id=1)
        assert p != None and p.name == "awesome" and p.owner_id == 1 and p.id == 1

    def test_get_pirg_by_name_awesome(self):
        from .crud import get_pirg_by_name

        p = get_pirg_by_name(self.db, "awesome")
        assert p != None and p.name == "awesome" and p.owner_id == 1 and p.id == 1

    def test_add_user_to_pirg_mike_to_awesome(self):
        from .crud import get_pirg_by_name, add_user_to_pirg, get_user_by_username

        p = get_pirg_by_name(self.db, name="awesome")
        u = get_user_by_username(self.db, username="mikem")
        p = add_user_to_pirg(self.db, pirg=p, user=u)
        assert len(p.users) == 1

    def test_remove_user_from_pirg_user_not_in_pirg(self):
        from .crud import get_pirg_by_name, remove_user_from_pirg, get_user_by_username

        p = get_pirg_by_name(self.db, name="awesome")
        u = get_user_by_username(self.db, username="mariem")
        p = remove_user_from_pirg(self.db, pirg=p, user=u)
        assert len(p.users) == 1

    def test_remove_user_from_pirg_mike_from_awesome(self):
        from .crud import get_pirg_by_name, remove_user_from_pirg, get_user_by_username

        p = get_pirg_by_name(self.db, name="awesome")
        u = get_user_by_username(self.db, username="mikem")
        p = remove_user_from_pirg(self.db, pirg=p, user=u)
        assert len(p.users) == 0

    def test_create_pirg_group_awesome_fancygroup(self):
        from .crud import get_pirg_by_name, create_pirg_group
        from ..api import schemas

        # add timmyt and mikem to awesome.fancygroup
        p = get_pirg_by_name(self.db, name="awesome")
        gc = schemas.GroupCreate(name="fancygroup", pirg_id=p.id, user_ids=[1, 2])
        pg = create_pirg_group(self.db, group=gc)
        assert len(pg.users) == 2

    def test_create_pirg_group_duplicate(self):
        from .crud import get_pirg_by_name, create_pirg_group, GroupAlreadyExistsError
        from ..api import schemas

        # add timmyt and mikem to awesome.fancygroup
        p = get_pirg_by_name(self.db, name="awesome")
        gc = schemas.GroupCreate(name="fancygroup", pirg_id=p.id, user_ids=[1, 2])
        with pytest.raises(GroupAlreadyExistsError):
            create_pirg_group(self.db, group=gc)

    def test_get_pirg_group_awesome_fancygroup(self):
        from .crud import get_pirg_group

        pg = get_pirg_group(self.db, group_id=1)
        assert pg != None and pg.name == "fancygroup" and len(pg.users) == 2

    def test_get_pirg_group_awesome_fancygroup_name(self):
        from .crud import get_pirg_by_name, get_pirg_group_by_name

        p = get_pirg_by_name(self.db, name="awesome")
        pg = get_pirg_group_by_name(self.db, pirg=p, name="fancygroup")
        assert pg != None and pg.name == "fancygroup" and len(pg.users) == 2

    def test_add_user_to_pirg_group_awesome_fancygroup_mariem(self):
        from .crud import get_pirg_group, add_user_to_pirg_group, get_user_by_username

        pg = get_pirg_group(self.db, group_id=1)
        u = get_user_by_username(self.db, username="mariem")
        pg = add_user_to_pirg_group(self.db, group=pg, user=u)
        assert len(pg.users) == 3

    def test_add_user_to_pirg_group_awesome_fancygroup_mariem_duplicate(self):
        from .crud import get_pirg_group, add_user_to_pirg_group, get_user_by_username

        pg = get_pirg_group(self.db, group_id=1)
        u = get_user_by_username(self.db, username="mariem")
        pg = add_user_to_pirg_group(self.db, group=pg, user=u)
        assert len(pg.users) == 3

    def test_remove_user_from_pirg_group_awesome_fancygroup_mariem(self):
        from .crud import (
            get_pirg_group,
            remove_user_from_pirg_group,
            get_user_by_username,
        )

        pg = get_pirg_group(self.db, group_id=1)
        u = get_user_by_username(self.db, username="mariem")
        pg = remove_user_from_pirg_group(self.db, group=pg, user=u)
        assert len(pg.users) == 2

    def test_delete_pirg_group_awesome_fancygroup(self):
        from .crud import get_pirg_group, delete_pirg_group

        pg = get_pirg_group(self.db, group_id=1)
        pg = delete_pirg_group(self.db, group=pg)
        assert pg == None

    def test_get_pirg_group_awesome_fancygroup_deleted(self):
        from .crud import get_pirg_group

        pg = get_pirg_group(self.db, group_id=1)
        assert pg == None
