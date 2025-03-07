# Code generated by jtd-codegen for Python v0.3.1

import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Union, get_args, get_origin


@dataclass
class LivestreamSchemaJtd:
    value: 'Account'

    @classmethod
    def from_json_data(cls, data: Any) -> 'LivestreamSchemaJtd':
        return cls(_from_json_data(Account, data))

    def to_json_data(self) -> Any:
        return _to_json_data(self.value)

@dataclass
class AccountFollowers:
    data: 'List[Account]'
    total: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'AccountFollowers':
        return cls(
            _from_json_data(List[Account], data.get("data")),
            _from_json_data(int, data.get("total")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["data"] = _to_json_data(self.data)
        data["total"] = _to_json_data(self.total)
        return data

@dataclass
class AccountFollowing:
    data: 'List[Account]'
    total: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'AccountFollowing':
        return cls(
            _from_json_data(List[Account], data.get("data")),
            _from_json_data(int, data.get("total")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["data"] = _to_json_data(self.data)
        data["total"] = _to_json_data(self.total)
        return data

@dataclass
class AccountLink:
    title: 'str'
    url: 'str'

    @classmethod
    def from_json_data(cls, data: Any) -> 'AccountLink':
        return cls(
            _from_json_data(str, data.get("title")),
            _from_json_data(str, data.get("url")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["title"] = _to_json_data(self.title)
        data["url"] = _to_json_data(self.url)
        return data

@dataclass
class AccountPastEvents:
    data: 'List[Event]'
    total: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'AccountPastEvents':
        return cls(
            _from_json_data(List[Event], data.get("data")),
            _from_json_data(int, data.get("total")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["data"] = _to_json_data(self.data)
        data["total"] = _to_json_data(self.total)
        return data

@dataclass
class AccountUpcomingEvents:
    data: 'List[Event]'
    total: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'AccountUpcomingEvents':
        return cls(
            _from_json_data(List[Event], data.get("data")),
            _from_json_data(int, data.get("total")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["data"] = _to_json_data(self.data)
        data["total"] = _to_json_data(self.total)
        return data

@dataclass
class Account:
    background_attachment: 'str'
    background_color: 'str'
    background_image: 'Image'
    background_position: 'str'
    background_repeat: 'str'
    category: 'int'
    category_name: 'Any'
    created_at: 'datetime'
    description: 'str'
    followers: 'AccountFollowers'
    following: 'AccountFollowing'
    full_name: 'str'
    google_analytics_id: 'str'
    id: 'int'
    is_beta_producer: 'bool'
    is_locked: 'bool'
    is_public: 'bool'
    is_searchable: 'bool'
    links: 'List[AccountLink]'
    mixpanel_id: 'str'
    past_events: 'AccountPastEvents'
    picture: 'Image'
    plan_id: 'int'
    private: 'bool'
    short_name: 'str'
    signup_action: 'str'
    signup_page: 'str'
    timezone: 'str'
    upcoming_events: 'AccountUpcomingEvents'

    @classmethod
    def from_json_data(cls, data: Any) -> 'Account':
        return cls(
            _from_json_data(str, data.get("background_attachment")),
            _from_json_data(str, data.get("background_color")),
            _from_json_data(Image, data.get("background_image")),
            _from_json_data(str, data.get("background_position")),
            _from_json_data(str, data.get("background_repeat")),
            _from_json_data(int, data.get("category")),
            _from_json_data(Any, data.get("category_name")),
            _from_json_data(datetime, data.get("created_at")),
            _from_json_data(str, data.get("description")),
            _from_json_data(AccountFollowers, data.get("followers")),
            _from_json_data(AccountFollowing, data.get("following")),
            _from_json_data(str, data.get("full_name")),
            _from_json_data(str, data.get("google_analytics_id")),
            _from_json_data(int, data.get("id")),
            _from_json_data(bool, data.get("is_beta_producer")),
            _from_json_data(bool, data.get("is_locked")),
            _from_json_data(bool, data.get("is_public")),
            _from_json_data(bool, data.get("is_searchable")),
            _from_json_data(List[AccountLink], data.get("links")),
            _from_json_data(str, data.get("mixpanel_id")),
            _from_json_data(AccountPastEvents, data.get("past_events")),
            _from_json_data(Image, data.get("picture")),
            _from_json_data(int, data.get("plan_id")),
            _from_json_data(bool, data.get("private")),
            _from_json_data(str, data.get("short_name")),
            _from_json_data(str, data.get("signup_action")),
            _from_json_data(str, data.get("signup_page")),
            _from_json_data(str, data.get("timezone")),
            _from_json_data(AccountUpcomingEvents, data.get("upcoming_events")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["background_attachment"] = _to_json_data(self.background_attachment)
        data["background_color"] = _to_json_data(self.background_color)
        data["background_image"] = _to_json_data(self.background_image)
        data["background_position"] = _to_json_data(self.background_position)
        data["background_repeat"] = _to_json_data(self.background_repeat)
        data["category"] = _to_json_data(self.category)
        data["category_name"] = _to_json_data(self.category_name)
        data["created_at"] = _to_json_data(self.created_at)
        data["description"] = _to_json_data(self.description)
        data["followers"] = _to_json_data(self.followers)
        data["following"] = _to_json_data(self.following)
        data["full_name"] = _to_json_data(self.full_name)
        data["google_analytics_id"] = _to_json_data(self.google_analytics_id)
        data["id"] = _to_json_data(self.id)
        data["is_beta_producer"] = _to_json_data(self.is_beta_producer)
        data["is_locked"] = _to_json_data(self.is_locked)
        data["is_public"] = _to_json_data(self.is_public)
        data["is_searchable"] = _to_json_data(self.is_searchable)
        data["links"] = _to_json_data(self.links)
        data["mixpanel_id"] = _to_json_data(self.mixpanel_id)
        data["past_events"] = _to_json_data(self.past_events)
        data["picture"] = _to_json_data(self.picture)
        data["plan_id"] = _to_json_data(self.plan_id)
        data["private"] = _to_json_data(self.private)
        data["short_name"] = _to_json_data(self.short_name)
        data["signup_action"] = _to_json_data(self.signup_action)
        data["signup_page"] = _to_json_data(self.signup_page)
        data["timezone"] = _to_json_data(self.timezone)
        data["upcoming_events"] = _to_json_data(self.upcoming_events)
        return data

@dataclass
class EventLikes:
    data: 'List[Any]'
    total: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'EventLikes':
        return cls(
            _from_json_data(List[Any], data.get("data")),
            _from_json_data(int, data.get("total")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["data"] = _to_json_data(self.data)
        data["total"] = _to_json_data(self.total)
        return data

@dataclass
class Event:
    activity_disabled: 'bool'
    background_attachment: 'Any'
    background_color: 'Optional[str]'
    background_image: 'Any'
    background_position: 'Any'
    background_repeat: 'Any'
    broadcast_id: 'int'
    created_at: 'datetime'
    description: 'str'
    draft: 'bool'
    embed_restriction: 'str'
    embed_restriction_blacklist: 'Any'
    embed_restriction_whitelist: 'List[str]'
    end_time: 'datetime'
    expires_at: 'Any'
    feed: 'Any'
    full_name: 'str'
    guest_chat_enabled: 'bool'
    id: 'int'
    in_progress: 'bool'
    is_donations_enabled: 'Any'
    is_embed_white_labeled: 'bool'
    is_embeddable: 'bool'
    is_likable: 'bool'
    is_password_protected: 'bool'
    is_public: 'bool'
    is_searchable: 'bool'
    is_white_labeled: 'bool'
    lat: 'float'
    likes: 'EventLikes'
    links: 'Any'
    live_chat_enabled: 'bool'
    live_video_post_id: 'int'
    lng: 'float'
    logo: 'Image'
    owner: 'Account'
    owner_account_id: 'int'
    post_comments_enabled: 'bool'
    post_count: 'Any'
    privacy_freeze: 'bool'
    real_time: 'Any'
    short_name: 'str'
    start_time: 'datetime'
    stream_info: 'Any'
    tags: 'Any'
    updated_at: 'datetime'
    video_count: 'Any'
    viewer_count: 'int'
    viewer_count_visible: 'bool'
    views_count: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'Event':
        return cls(
            _from_json_data(bool, data.get("activity_disabled")),
            _from_json_data(Any, data.get("background_attachment")),
            _from_json_data(Optional[str], data.get("background_color")),
            _from_json_data(Any, data.get("background_image")),
            _from_json_data(Any, data.get("background_position")),
            _from_json_data(Any, data.get("background_repeat")),
            _from_json_data(int, data.get("broadcast_id")),
            _from_json_data(datetime, data.get("created_at")),
            _from_json_data(str, data.get("description")),
            _from_json_data(bool, data.get("draft")),
            _from_json_data(str, data.get("embed_restriction")),
            _from_json_data(Any, data.get("embed_restriction_blacklist")),
            _from_json_data(List[str], data.get("embed_restriction_whitelist")),
            _from_json_data(datetime, data.get("end_time")),
            _from_json_data(Any, data.get("expires_at")),
            _from_json_data(Any, data.get("feed")),
            _from_json_data(str, data.get("full_name")),
            _from_json_data(bool, data.get("guest_chat_enabled")),
            _from_json_data(int, data.get("id")),
            _from_json_data(bool, data.get("in_progress")),
            _from_json_data(Any, data.get("is_donations_enabled")),
            _from_json_data(bool, data.get("is_embed_white_labeled")),
            _from_json_data(bool, data.get("is_embeddable")),
            _from_json_data(bool, data.get("is_likable")),
            _from_json_data(bool, data.get("is_password_protected")),
            _from_json_data(bool, data.get("is_public")),
            _from_json_data(bool, data.get("is_searchable")),
            _from_json_data(bool, data.get("is_white_labeled")),
            _from_json_data(float, data.get("lat")),
            _from_json_data(EventLikes, data.get("likes")),
            _from_json_data(Any, data.get("links")),
            _from_json_data(bool, data.get("live_chat_enabled")),
            _from_json_data(int, data.get("live_video_post_id")),
            _from_json_data(float, data.get("lng")),
            _from_json_data(Image, data.get("logo")),
            _from_json_data(Account, data.get("owner")),
            _from_json_data(int, data.get("owner_account_id")),
            _from_json_data(bool, data.get("post_comments_enabled")),
            _from_json_data(Any, data.get("post_count")),
            _from_json_data(bool, data.get("privacy_freeze")),
            _from_json_data(Any, data.get("real_time")),
            _from_json_data(str, data.get("short_name")),
            _from_json_data(datetime, data.get("start_time")),
            _from_json_data(Any, data.get("stream_info")),
            _from_json_data(Any, data.get("tags")),
            _from_json_data(datetime, data.get("updated_at")),
            _from_json_data(Any, data.get("video_count")),
            _from_json_data(int, data.get("viewer_count")),
            _from_json_data(bool, data.get("viewer_count_visible")),
            _from_json_data(int, data.get("views_count")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["activity_disabled"] = _to_json_data(self.activity_disabled)
        data["background_attachment"] = _to_json_data(self.background_attachment)
        data["background_color"] = _to_json_data(self.background_color)
        data["background_image"] = _to_json_data(self.background_image)
        data["background_position"] = _to_json_data(self.background_position)
        data["background_repeat"] = _to_json_data(self.background_repeat)
        data["broadcast_id"] = _to_json_data(self.broadcast_id)
        data["created_at"] = _to_json_data(self.created_at)
        data["description"] = _to_json_data(self.description)
        data["draft"] = _to_json_data(self.draft)
        data["embed_restriction"] = _to_json_data(self.embed_restriction)
        data["embed_restriction_blacklist"] = _to_json_data(self.embed_restriction_blacklist)
        data["embed_restriction_whitelist"] = _to_json_data(self.embed_restriction_whitelist)
        data["end_time"] = _to_json_data(self.end_time)
        data["expires_at"] = _to_json_data(self.expires_at)
        data["feed"] = _to_json_data(self.feed)
        data["full_name"] = _to_json_data(self.full_name)
        data["guest_chat_enabled"] = _to_json_data(self.guest_chat_enabled)
        data["id"] = _to_json_data(self.id)
        data["in_progress"] = _to_json_data(self.in_progress)
        data["is_donations_enabled"] = _to_json_data(self.is_donations_enabled)
        data["is_embed_white_labeled"] = _to_json_data(self.is_embed_white_labeled)
        data["is_embeddable"] = _to_json_data(self.is_embeddable)
        data["is_likable"] = _to_json_data(self.is_likable)
        data["is_password_protected"] = _to_json_data(self.is_password_protected)
        data["is_public"] = _to_json_data(self.is_public)
        data["is_searchable"] = _to_json_data(self.is_searchable)
        data["is_white_labeled"] = _to_json_data(self.is_white_labeled)
        data["lat"] = _to_json_data(self.lat)
        data["likes"] = _to_json_data(self.likes)
        data["links"] = _to_json_data(self.links)
        data["live_chat_enabled"] = _to_json_data(self.live_chat_enabled)
        data["live_video_post_id"] = _to_json_data(self.live_video_post_id)
        data["lng"] = _to_json_data(self.lng)
        data["logo"] = _to_json_data(self.logo)
        data["owner"] = _to_json_data(self.owner)
        data["owner_account_id"] = _to_json_data(self.owner_account_id)
        data["post_comments_enabled"] = _to_json_data(self.post_comments_enabled)
        data["post_count"] = _to_json_data(self.post_count)
        data["privacy_freeze"] = _to_json_data(self.privacy_freeze)
        data["real_time"] = _to_json_data(self.real_time)
        data["short_name"] = _to_json_data(self.short_name)
        data["start_time"] = _to_json_data(self.start_time)
        data["stream_info"] = _to_json_data(self.stream_info)
        data["tags"] = _to_json_data(self.tags)
        data["updated_at"] = _to_json_data(self.updated_at)
        data["video_count"] = _to_json_data(self.video_count)
        data["viewer_count"] = _to_json_data(self.viewer_count)
        data["viewer_count_visible"] = _to_json_data(self.viewer_count_visible)
        data["views_count"] = _to_json_data(self.views_count)
        return data

@dataclass
class Image:
    height: 'int'
    medium_url: 'Any'
    original_height: 'int'
    original_width: 'int'
    secure_medium_url: 'Any'
    secure_small_url: 'str'
    secure_thumb_url: 'Any'
    small_url: 'str'
    thumb_url: 'Any'
    url: 'str'
    width: 'int'

    @classmethod
    def from_json_data(cls, data: Any) -> 'Image':
        return cls(
            _from_json_data(int, data.get("height")),
            _from_json_data(Any, data.get("medium_url")),
            _from_json_data(int, data.get("original_height")),
            _from_json_data(int, data.get("original_width")),
            _from_json_data(Any, data.get("secure_medium_url")),
            _from_json_data(str, data.get("secure_small_url")),
            _from_json_data(Any, data.get("secure_thumb_url")),
            _from_json_data(str, data.get("small_url")),
            _from_json_data(Any, data.get("thumb_url")),
            _from_json_data(str, data.get("url")),
            _from_json_data(int, data.get("width")),
        )

    def to_json_data(self) -> Any:
        data: Dict[str, Any] = {}
        data["height"] = _to_json_data(self.height)
        data["medium_url"] = _to_json_data(self.medium_url)
        data["original_height"] = _to_json_data(self.original_height)
        data["original_width"] = _to_json_data(self.original_width)
        data["secure_medium_url"] = _to_json_data(self.secure_medium_url)
        data["secure_small_url"] = _to_json_data(self.secure_small_url)
        data["secure_thumb_url"] = _to_json_data(self.secure_thumb_url)
        data["small_url"] = _to_json_data(self.small_url)
        data["thumb_url"] = _to_json_data(self.thumb_url)
        data["url"] = _to_json_data(self.url)
        data["width"] = _to_json_data(self.width)
        return data

def _from_json_data(cls: Any, data: Any) -> Any:
    if data is None or cls in [bool, int, float, str, object] or cls is Any:
        return data
    if cls is datetime:
        return _parse_rfc3339(data)
    if get_origin(cls) is Union:
        return _from_json_data(get_args(cls)[0], data)
    if get_origin(cls) is list:
        return [_from_json_data(get_args(cls)[0], d) for d in data]
    if get_origin(cls) is dict:
        return { k: _from_json_data(get_args(cls)[1], v) for k, v in data.items() }
    return cls.from_json_data(data)

def _to_json_data(data: Any) -> Any:
    if data is None or type(data) in [bool, int, float, str, object]:
        return data
    if type(data) is datetime:
        return data.isoformat()
    if type(data) is list:
        return [_to_json_data(d) for d in data]
    if type(data) is dict:
        return { k: _to_json_data(v) for k, v in data.items() }
    return data.to_json_data()

def _parse_rfc3339(s: str) -> datetime:
    datetime_re = '^(\d{4})-(\d{2})-(\d{2})[tT](\d{2}):(\d{2}):(\d{2})(\.\d+)?([zZ]|((\+|-)(\d{2}):(\d{2})))$'
    match = re.match(datetime_re, s)
    if not match:
        raise ValueError('Invalid RFC3339 date/time', s)

    (year, month, day, hour, minute, second, frac_seconds, offset,
     *tz) = match.groups()

    frac_seconds_parsed = None
    if frac_seconds:
        frac_seconds_parsed = int(float(frac_seconds) * 1_000_000)
    else:
        frac_seconds_parsed = 0

    tzinfo = None
    if offset == 'Z':
        tzinfo = timezone.utc
    else:
        hours = int(tz[2])
        minutes = int(tz[3])
        sign = 1 if tz[1] == '+' else -1

        if minutes not in range(60):
            raise ValueError('minute offset must be in 0..59')

        tzinfo = timezone(timedelta(minutes=sign * (60 * hours + minutes)))

    second_parsed = int(second)
    if second_parsed == 60:
        second_parsed = 59

    return datetime(int(year), int(month), int(day), int(hour), int(minute),
                    second_parsed, frac_seconds_parsed, tzinfo)            
