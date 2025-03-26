from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from pymongo.collection import Collection

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["sms_platform_v2"]

class Collections:
    campaign: Collection = db["campaign"]
    ussd_service: Collection = db["ussd_service"]
    shortcode: Collection = db["shortcode"]
    analytic: Collection = db["analytic"]
    otp: Collection = db["otp"]
    gateway: Collection = db["gateway"]
    user: Collection = db["user"]
    scheduler: Collection = db["scheduler"]
    service: Collection = db["service"]
    ticket: Collection = db["ticket"]
    payment: Collection = db["payment"]
    profile: Collection = db["profile"]
    permission: Collection = db["permission"]
    order: Collection = db["order"]
    support: Collection = db["support"]  # New collection

# Pydantic Models with id_mongo instead of _id
class Campaign(BaseModel):
    id: str = Field(..., description="Unique campaign identifier")
    nm: str = Field(..., min_length=1, max_length=100)
    ds: str = Field(..., max_length=500)
    start_dt: datetime = Field(..., description="Campaign start date")
    end_dt: datetime = Field(..., description="Campaign end date")
    target_audience: List[str] = Field(..., min_items=1)
    status: str = Field(..., pattern="^(active|completed|scheduled)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class USSDService(BaseModel):
    cd: str = Field(..., pattern=r"^\*[0-9]+(\*[0-9]+)*#$", description="USSD code")
    ds: str = Field(..., max_length=200)
    menu_options: List[str] = Field(..., min_items=1)
    session_timeout: int = Field(..., ge=30, le=300)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Shortcode(BaseModel):
    cd: str = Field(..., pattern=r"^[0-9]{4,6}$", description="Shortcode")
    type: str = Field(..., pattern="^(dedicated|shared)$")
    ds: str = Field(..., max_length=200)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Analytics(BaseModel):
    campaign_id: str = Field(..., description="Reference to campaign")
    delivery_rt: float = Field(..., ge=0.0, le=100.0)
    metrics: dict = Field(..., description="Engagement stats")
    timestamp_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class OTPAuthentication(BaseModel):
    user_id: str = Field(..., description="Reference to user")
    cd: str = Field(..., pattern=r"^[0-9]{6}$", description="6-digit OTP")
    expiry_dt: datetime = Field(...)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class SMSGateway(BaseModel):
    id: str = Field(..., description="Unique gateway ID")
    nm: str = Field(..., max_length=100)
    api_endpoint: str = Field(..., description="Gateway API URL")
    api_key: str = Field(..., min_length=10)
    status: str = Field(..., pattern="^(active|inactive)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class User(BaseModel):
    id: str = Field(..., description="Unique user identifier")
    nm: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    phone_nb: str = Field(..., pattern=r"^\+[1-9]\d{1,14}$")
    role: str = Field(..., pattern="^(admin|user)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Scheduler(BaseModel):
    id: str = Field(..., description="Unique scheduler ID")
    nm: str = Field(..., max_length=100)
    ds: str = Field(..., max_length=500)
    campaign_id: Optional[str] = Field(None, description="Reference to campaign")
    schedule_dt: datetime = Field(...)
    status: str = Field(..., pattern="^(pending|completed|failed)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Service(BaseModel):
    id: str = Field(..., description="Unique service ID")
    nm: str = Field(..., max_length=100)
    ds: str = Field(..., max_length=200)
    type: str = Field(..., pattern="^(sms|ussd)$")
    status: str = Field(..., pattern="^(active|inactive)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Ticket(BaseModel):
    id: str = Field(..., description="Unique ticket ID")
    user_id: str = Field(..., description="Reference to user")
    ds: str = Field(..., max_length=500)
    status: str = Field(..., pattern="^(open|resolved|closed)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    resolved_dt: Optional[datetime] = Field(None)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Payment(BaseModel):
    id: str = Field(..., description="Unique payment ID")
    user_id: str = Field(..., description="Reference to user")
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern="^[A-Z]{3}$")
    status: str = Field(..., pattern="^(pending|completed|failed)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Profile(BaseModel):
    id: str = Field(..., description="Unique profile ID")
    user_id: str = Field(..., description="Reference to user")
    full_nm: str = Field(..., max_length=100)
    address: Optional[str] = Field(None, max_length=200)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Permission(BaseModel):
    id: str = Field(..., description="Unique permission ID")
    nm: str = Field(..., max_length=50)
    ds: str = Field(..., max_length=200)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Order(BaseModel):
    id: str = Field(..., description="Unique order ID")
    user_id: str = Field(..., description="Reference to user")
    service_id: str = Field(..., description="Reference to service")
    amount: float = Field(..., gt=0)
    status: str = Field(..., pattern="^(pending|completed)$")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

class Support(BaseModel):  # New model
    id: str = Field(..., description="Unique support request ID")
    user_id: str = Field(..., description="Reference to user")
    ds: str = Field(..., max_length=500, description="Description of the support issue")
    category: str = Field(..., pattern="^(billing|technical|general)$", description="Support category")
    status: str = Field(..., pattern="^(open|in_progress|resolved)$", description="Support status")
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    id_mongo: Optional[str] = Field(None, description="MongoDB ObjectId")

# Create Indexes
Collections.campaign.create_index([("id", 1)], unique=True)
Collections.ussd_service.create_index([("cd", 1)], unique=True)
Collections.shortcode.create_index([("cd", 1)], unique=True)
Collections.analytic.create_index([("campaign_id", 1)])
Collections.otp.create_index([("user_id", 1)])
Collections.gateway.create_index([("id", 1)], unique=True)
Collections.user.create_index([("id", 1)], unique=True)
Collections.user.create_index([("email", 1)], unique=True)
Collections.scheduler.create_index([("id", 1)], unique=True)
Collections.service.create_index([("id", 1)], unique=True)
Collections.ticket.create_index([("id", 1)], unique=True)
Collections.payment.create_index([("id", 1)], unique=True)
Collections.profile.create_index([("id", 1)], unique=True)
Collections.permission.create_index([("id", 1)], unique=True)
Collections.order.create_index([("id", 1)], unique=True)
Collections.support.create_index([("id", 1)], unique=True)  # New index

# Campaign Endpoints
@app.post("/campaigns/", response_model=Campaign)
async def create_campaign(campaign: Campaign):
    campaign_dict = campaign.model_dump()
    if Collections.campaign.find_one({"id": campaign.id}):
        raise HTTPException(status_code=400, detail="Campaign ID already exists")
    result = Collections.campaign.insert_one(campaign_dict)
    campaign.id_mongo = str(result.inserted_id)
    return campaign

@app.get("/campaigns/{id}", response_model=Campaign)
async def read_campaign(id: str):
    campaign = Collections.campaign.find_one({"id": id})
    if campaign:
        campaign["id_mongo"] = str(campaign.pop("_id"))
        return campaign
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.put("/campaigns/{id}", response_model=Campaign)
async def update_campaign(id: str, campaign: Campaign):
    campaign_dict = campaign.model_dump(exclude={"id_mongo"})
    result = Collections.campaign.update_one({"id": id}, {"$set": campaign_dict})
    if result.matched_count:
        campaign.id_mongo = str(Collections.campaign.find_one({"id": id})["_id"])
        return campaign
    raise HTTPException(status_code=404, detail="Campaign not found")

@app.delete("/campaigns/{id}")
async def delete_campaign(id: str):
    result = Collections.campaign.delete_one({"id": id})
    if result.deleted_count:
        return {"message": "Campaign deleted"}
    raise HTTPException(status_code=404, detail="Campaign not found")

# USSD Service Endpoints
@app.post("/ussd-services/", response_model=USSDService)
async def create_ussd_service(ussd_service: USSDService):
    ussd_dict = ussd_service.model_dump()
    if Collections.ussd_service.find_one({"cd": ussd_service.cd}):
        raise HTTPException(status_code=400, detail="USSD code already exists")
    result = Collections.ussd_service.insert_one(ussd_dict)
    ussd_service.id_mongo = str(result.inserted_id)
    return ussd_service

@app.get("/ussd-services/{cd}", response_model=USSDService)
async def read_ussd_service(cd: str):
    ussd = Collections.ussd_service.find_one({"cd": cd})
    if ussd:
        ussd["id_mongo"] = str(ussd.pop("_id"))
        return ussd
    raise HTTPException(status_code=404, detail="USSD Service not found")

@app.put("/ussd-services/{cd}", response_model=USSDService)
async def update_ussd_service(cd: str, ussd_service: USSDService):
    ussd_dict = ussd_service.model_dump(exclude={"id_mongo"})
    result = Collections.ussd_service.update_one({"cd": cd}, {"$set": ussd_dict})
    if result.matched_count:
        ussd_service.id_mongo = str(Collections.ussd_service.find_one({"cd": cd})["_id"])
        return ussd_service
    raise HTTPException(status_code=404, detail="USSD Service not found")

@app.delete("/ussd-services/{cd}")
async def delete_ussd_service(cd: str):
    result = Collections.ussd_service.delete_one({"cd": cd})
    if result.deleted_count:
        return {"message": "USSD Service deleted"}
    raise HTTPException(status_code=404, detail="USSD Service not found")

# Shortcode Endpoints
@app.post("/shortcodes/", response_model=Shortcode)
async def create_shortcode(shortcode: Shortcode):
    shortcode_dict = shortcode.model_dump()
    if Collections.shortcode.find_one({"cd": shortcode.cd}):
        raise HTTPException(status_code=400, detail="Shortcode already exists")
    result = Collections.shortcode.insert_one(shortcode_dict)
    shortcode.id_mongo = str(result.inserted_id)
    return shortcode

@app.get("/shortcodes/{cd}", response_model=Shortcode)
async def read_shortcode(cd: str):
    short = Collections.shortcode.find_one({"cd": cd})
    if short:
        short["id_mongo"] = str(short.pop("_id"))
        return short
    raise HTTPException(status_code=404, detail="Shortcode not found")

@app.put("/shortcodes/{cd}", response_model=Shortcode)
async def update_shortcode(cd: str, shortcode_data: Shortcode):
    shortcode_dict = shortcode_data.model_dump(exclude={"id_mongo"})
    result = Collections.shortcode.update_one({"cd": cd}, {"$set": shortcode_dict})
    if result.matched_count:
        shortcode_data.id_mongo = str(Collections.shortcode.find_one({"cd": cd})["_id"])
        return shortcode_data
    raise HTTPException(status_code=404, detail="Shortcode not found")

@app.delete("/shortcodes/{cd}")
async def delete_shortcode(cd: str):
    result = Collections.shortcode.delete_one({"cd": cd})
    if result.deleted_count:
        return {"message": "Shortcode deleted"}
    raise HTTPException(status_code=404, detail="Shortcode not found")

# Analytics Endpoints
@app.post("/analytics/", response_model=Analytics)
async def create_analytics(analytics: Analytics):
    analytics_dict = analytics.model_dump()
    result = Collections.analytic.insert_one(analytics_dict)
    analytics.id_mongo = str(result.inserted_id)
    return analytics

@app.get("/analytics/{campaign_id}", response_model=Analytics)
async def read_analytics(campaign_id: str):
    analytics = Collections.analytic.find_one({"campaign_id": campaign_id})
    if analytics:
        analytics["id_mongo"] = str(analytics.pop("_id"))
        return analytics
    raise HTTPException(status_code=404, detail="Analytics not found")

# OTP Endpoints
@app.post("/otp/", response_model=OTPAuthentication)
async def create_otp(otp: OTPAuthentication):
    otp_dict = otp.model_dump()
    result = Collections.otp.insert_one(otp_dict)
    otp.id_mongo = str(result.inserted_id)
    return otp

@app.get("/otp/{user_id}", response_model=OTPAuthentication)
async def read_otp(user_id: str):
    otp = Collections.otp.find_one({"user_id": user_id})
    if otp:
        otp["id_mongo"] = str(otp.pop("_id"))
        return otp
    raise HTTPException(status_code=404, detail="OTP not found")

@app.delete("/otp/{user_id}")
async def delete_otp(user_id: str):
    result = Collections.otp.delete_one({"user_id": user_id})
    if result.deleted_count:
        return {"message": "OTP deleted"}
    raise HTTPException(status_code=404, detail="OTP not found")

# SMS Gateway Endpoints
@app.post("/sms-gateways/", response_model=SMSGateway)
async def create_sms_gateway(gateway: SMSGateway):
    gateway_dict = gateway.model_dump()
    if Collections.gateway.find_one({"id": gateway.id}):
        raise HTTPException(status_code=400, detail="Gateway ID already exists")
    result = Collections.gateway.insert_one(gateway_dict)
    gateway.id_mongo = str(result.inserted_id)
    return gateway

@app.get("/sms-gateways/{id}", response_model=SMSGateway)
async def read_sms_gateway(id: str):
    gateway = Collections.gateway.find_one({"id": id})
    if gateway:
        gateway["id_mongo"] = str(gateway.pop("_id"))
        return gateway
    raise HTTPException(status_code=404, detail="SMS Gateway not found")

@app.put("/sms-gateways/{id}", response_model=SMSGateway)
async def update_sms_gateway(id: str, gateway: SMSGateway):
    gateway_dict = gateway.model_dump(exclude={"id_mongo"})
    result = Collections.gateway.update_one({"id": id}, {"$set": gateway_dict})
    if result.matched_count:
        gateway.id_mongo = str(Collections.gateway.find_one({"id": id})["_id"])
        return gateway
    raise HTTPException(status_code=404, detail="SMS Gateway not found")

@app.delete("/sms-gateways/{id}")
async def delete_sms_gateway(id: str):
    result = Collections.gateway.delete_one({"id": id})
    if result.deleted_count:
        return {"message": "SMS Gateway deleted"}
    raise HTTPException(status_code=404, detail="SMS Gateway not found")

# User Endpoints
@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_dict = user.model_dump()
    if Collections.user.find_one({"id": user.id}) or \
       Collections.user.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User ID or email already exists")
    result = Collections.user.insert_one(user_dict)
    user.id_mongo = str(result.inserted_id)
    return user

@app.get("/users/{id}", response_model=User)
async def read_user(id: str):
    user = Collections.user.find_one({"id": id})
    if user:
        user["id_mongo"] = str(user.pop("_id"))
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{id}", response_model=User)
async def update_user(id: str, user: User):
    user_dict = user.model_dump(exclude={"id_mongo"})
    result = Collections.user.update_one({"id": id}, {"$set": user_dict})
    if result.matched_count:
        user.id_mongo = str(Collections.user.find_one({"id": id})["_id"])
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}")
async def delete_user(id: str):
    result = Collections.user.delete_one({"id": id})
    if result.deleted_count:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

# Scheduler Endpoints
@app.post("/scheduler/", response_model=Scheduler)
async def create_scheduler(scheduler: Scheduler):
    scheduler_dict = scheduler.model_dump()
    if Collections.scheduler.find_one({"id": scheduler.id}):
        raise HTTPException(status_code=400, detail="Scheduler ID already exists")
    result = Collections.scheduler.insert_one(scheduler_dict)
    scheduler.id_mongo = str(result.inserted_id)
    return scheduler

# Service Endpoints
@app.post("/service/", response_model=Service)
async def create_service(service: Service):
    service_dict = service.model_dump()
    if Collections.service.find_one({"id": service.id}):
        raise HTTPException(status_code=400, detail="Service ID already exists")
    result = Collections.service.insert_one(service_dict)
    service.id_mongo = str(result.inserted_id)
    return service

# Ticket Endpoints
@app.post("/ticket/", response_model=Ticket)
async def create_ticket(ticket: Ticket):
    ticket_dict = ticket.model_dump()
    if Collections.ticket.find_one({"id": ticket.id}):
        raise HTTPException(status_code=400, detail="Ticket ID already exists")
    result = Collections.ticket.insert_one(ticket_dict)
    ticket.id_mongo = str(result.inserted_id)
    return ticket

# Payment Endpoints
@app.post("/payment/", response_model=Payment)
async def create_payment(payment: Payment):
    payment_dict = payment.model_dump()
    if Collections.payment.find_one({"id": payment.id}):
        raise HTTPException(status_code=400, detail="Payment ID already exists")
    result = Collections.payment.insert_one(payment_dict)
    payment.id_mongo = str(result.inserted_id)
    return payment

# Profile Endpoints
@app.post("/profile/", response_model=Profile)
async def create_profile(profile: Profile):
    profile_dict = profile.model_dump()
    if Collections.profile.find_one({"id": profile.id}):
        raise HTTPException(status_code=400, detail="Profile ID already exists")
    result = Collections.profile.insert_one(profile_dict)
    profile.id_mongo = str(result.inserted_id)
    return profile

# Permission Endpoints
@app.post("/permission/", response_model=Permission)
async def create_permission(permission: Permission):
    permission_dict = permission.model_dump()
    if Collections.permission.find_one({"id": permission.id}):
        raise HTTPException(status_code=400, detail="Permission ID already exists")
    result = Collections.permission.insert_one(permission_dict)
    permission.id_mongo = str(result.inserted_id)
    return permission

# Order Endpoints
@app.post("/order/", response_model=Order)
async def create_order(order: Order):
    order_dict = order.model_dump()
    if Collections.order.find_one({"id": order.id}):
        raise HTTPException(status_code=400, detail="Order ID already exists")
    result = Collections.order.insert_one(order_dict)
    order.id_mongo = str(result.inserted_id)
    return order

# Support Endpoints (New)
@app.post("/support/", response_model=Support)
async def create_support(support: Support):
    support_dict = support.model_dump()
    if Collections.support.find_one({"id": support.id}):
        raise HTTPException(status_code=400, detail="Support ID already exists")
    result = Collections.support.insert_one(support_dict)
    support.id_mongo = str(result.inserted_id)
    return support

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)