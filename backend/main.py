"""
MMORPG Store Module - FastAPI Backend
MongoDB ile bakiye, item ve envanter yönetimi
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
import asyncio
import os

app = FastAPI(title="MMORPG Store API", version="1.0.0")

# CORS - Chromium frontend erişimi için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB bağlantısı
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client["mmorpg_store"]

# Koleksiyonlar
players_col = db["players"]
items_col = db["items"]
purchases_col = db["purchases"]


# ─────────────────────────────────────────────
# Pydantic Modeller
# ─────────────────────────────────────────────

class BuyRequest(BaseModel):
    player_id: str
    item_id: str


# ─────────────────────────────────────────────
# Başlangıç Verisi - DB yoksa oluştur
# ─────────────────────────────────────────────

INITIAL_ITEMS = [
    {
        "_id": "item_001",
        "name": "Ejder Nefesi Kılıcı",
        "description": "Bin yıllık ejder ruhunun hapsedildiği kılıç. Her vuruşta kor alevi saçar. Saldırı +180.",
        "category": "Silahlar",
        "price": 650,
        "rarity": "legendary",
        "icon": "sword_fire",
        "stock": -1,
        "popular": True,
    },
    {
        "_id": "item_002",
        "name": "Hanedanlık Kalkanı",
        "description": "Çin hanedanlığının demircileri tarafından dövülen kutsal kalkan. Tüm hasar yansıtma %15.",
        "category": "Kalkanlar",
        "price": 820,
        "rarity": "legendary",
        "icon": "shield_dragon",
        "stock": -1,
        "popular": True,
    },
    {
        "_id": "item_003",
        "name": "Yeşim Can Taşı",
        "description": "Kutsal dağlardan çıkarılan saf yeşim. Giyildiğinde ruhu besler. Maksimum can +600.",
        "category": "Taşlar",
        "price": 340,
        "rarity": "epic",
        "icon": "gem_life",
        "stock": -1,
        "popular": True,
    },
    {
        "_id": "item_004",
        "name": "Altın Fener Anahtarı",
        "description": "Ejder tapınağının kapalı odalarını açar. Her kapının arkasında bir sır vardır.",
        "category": "Öğeler",
        "price": 180,
        "rarity": "rare",
        "icon": "key_golden",
        "stock": -1,
        "popular": False,
        "discount": 60,
    },
    {
        "_id": "item_005",
        "name": "Ay Çiyi Paketi (10.000)",
        "description": "10.000 Adet Ay Çiyi. Büyü tılsımlarını güçlendirmek ve zırh parlatmak için kullanılır.",
        "category": "Taşlar",
        "price": 240,
        "rarity": "common",
        "icon": "stone_water",
        "stock": -1,
        "popular": False,
        "discount": 50,
    },
    {
        "_id": "item_006",
        "name": "Pirinç Külçe Paketi (5.000)",
        "description": "5.000 Adet Pirinç Külçe. Üretim atölyesinde ekipman yükseltmek için temel hammadde.",
        "category": "Öğeler",
        "price": 195,
        "rarity": "common",
        "icon": "bar_pack",
        "stock": -1,
        "popular": False,
        "discount": 55,
    },
    {
        "_id": "item_007",
        "name": "Gece Kaplanı Zırhı",
        "description": "Efsanevi kaplan ruhunu hapsetmek için örülmüş zırh. Hız +40, Savunma +280.",
        "category": "Zırhlar",
        "price": 1100,
        "rarity": "legendary",
        "icon": "armor_dark",
        "stock": -1,
        "popular": False,
    },
    {
        "_id": "item_008",
        "name": "Yedi Ejder Koruma Tılsımı",
        "description": "Yedi ejder enerjisiyle mühürlenmiş taş. Canavar büyülerine karşı tam koruma sağlar.",
        "category": "Taşlar",
        "price": 420,
        "rarity": "epic",
        "icon": "gem_ward",
        "stock": -1,
        "popular": True,
    },
    {
        "_id": "item_009",
        "name": "Lotüs Şerbeti Paketi (200)",
        "description": "200 Adet Saf Lotüs Şerbeti. Her yudumda can yenilenir, zehir etkisi temizlenir.",
        "category": "Öğeler",
        "price": 160,
        "rarity": "common",
        "icon": "fish_grilled",
        "stock": -1,
        "popular": True,
    },
    {
        "_id": "item_010",
        "name": "Gök Gürültüsü Yayı",
        "description": "Şimşek tanrısının nefesiyle yüklenmiş yay. Her ok bir fırtına taşır. Hız +55.",
        "category": "Silahlar",
        "price": 890,
        "rarity": "legendary",
        "icon": "bow_thunder",
        "stock": -1,
        "popular": False,
    },
    {
        "_id": "item_011",
        "name": "Ölümsüz Ruh Taşı (500)",
        "description": "500 Adet Ölümsüz Ruh Taşı. Ki enerjisini yoğunlaştırır, tüm büyü gücünü %20 artırır.",
        "category": "Taşlar",
        "price": 310,
        "rarity": "rare",
        "icon": "stone_soul",
        "stock": -1,
        "popular": False,
    },
    {
        "_id": "item_012",
        "name": "Ejder Hanedanlığı Mührü",
        "description": "Antik hanedanlığın imparator yüzüğü. Taktığında tüm savaşçılar seni duyar. Tüm stat +30.",
        "category": "İç Temler",
        "price": 680,
        "rarity": "epic",
        "icon": "ring_dragon",
        "stock": -1,
        "popular": False,
    },
]

INITIAL_PLAYER = {
    "_id": "player_001",
    "name": "Oyuncu",
    "sp_balance": 5000,   # SP (prim para)
    "sm_balance": 1000,   # SM (ikincil para)
}


@app.on_event("startup")
async def startup_db():
    """Veritabanı başlangıç verilerini yükle"""
    # Oyuncu yoksa oluştur
    existing_player = await players_col.find_one({"_id": "player_001"})
    if not existing_player:
        await players_col.insert_one(INITIAL_PLAYER)
        print("✅ Başlangıç oyuncusu oluşturuldu.")

    # Itemlar yoksa ekle
    item_count = await items_col.count_documents({})
    if item_count == 0:
        await items_col.insert_many(INITIAL_ITEMS)
        print(f"✅ {len(INITIAL_ITEMS)} item veritabanına eklendi.")

    print("🚀 MMORPG Store API başlatıldı!")


# ─────────────────────────────────────────────
# API Endpoint'leri
# ─────────────────────────────────────────────

@app.get("/api/player/{player_id}")
async def get_player(player_id: str):
    """Oyuncu bilgilerini getir (bakiye dahil)"""
    player = await players_col.find_one({"_id": player_id})
    if not player:
        raise HTTPException(status_code=404, detail="Oyuncu bulunamadı")
    return {
        "id": player["_id"],
        "name": player["name"],
        "sp_balance": player["sp_balance"],
        "sm_balance": player["sm_balance"],
    }


@app.get("/api/items")
async def get_items(category: Optional[str] = None):
    """Tüm mağaza itemlarını listele, isteğe bağlı kategori filtresi"""
    query = {}
    if category and category != "Tümü":
        query["category"] = category
    
    cursor = items_col.find(query)
    items = []
    async for item in cursor:
        items.append({
            "id": item["_id"],
            "name": item["name"],
            "description": item["description"],
            "category": item["category"],
            "price": item["price"],
            "rarity": item["rarity"],
            "icon": item["icon"],
            "popular": item.get("popular", False),
            "discount": item.get("discount", 0),
        })
    return items


@app.get("/api/purchases/{player_id}")
async def get_purchases(player_id: str):
    """Oyuncunun satın aldığı itemları getir (envanter)"""
    cursor = purchases_col.find({"player_id": player_id})
    purchases = []
    async for p in cursor:
        purchases.append({
            "id": str(p["_id"]),
            "item_id": p["item_id"],
            "item_name": p["item_name"],
            "item_icon": p["item_icon"],
            "item_rarity": p["item_rarity"],
            "price_paid": p["price_paid"],
            "quantity": p.get("quantity", 1),
            "purchased_at": p["purchased_at"].isoformat() if hasattr(p["purchased_at"], "isoformat") else str(p["purchased_at"]),
        })
    return purchases


@app.post("/api/buy")
async def buy_item(req: BuyRequest):
    """Item satın al - bakiye düş, envantere ekle"""
    # Oyuncuyu bul
    player = await players_col.find_one({"_id": req.player_id})
    if not player:
        raise HTTPException(status_code=404, detail="Oyuncu bulunamadı")

    # Itemi bul
    item = await items_col.find_one({"_id": req.item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item bulunamadı")

    # Bakiye kontrolü
    if player["sp_balance"] < item["price"]:
        raise HTTPException(
            status_code=400,
            detail=f"Yetersiz bakiye! Gerekli: {item['price']} SP, Mevcut: {player['sp_balance']} SP"
        )

    # Bakiyeyi düş
    new_balance = player["sp_balance"] - item["price"]
    await players_col.update_one(
        {"_id": req.player_id},
        {"$set": {"sp_balance": new_balance}}
    )

    # Satın alınanlar koleksiyonuna ekle
    from datetime import datetime
    
    # Zaten almışsa miktarı artır
    existing = await purchases_col.find_one({
        "player_id": req.player_id,
        "item_id": req.item_id
    })
    
    if existing:
        await purchases_col.update_one(
            {"player_id": req.player_id, "item_id": req.item_id},
            {"$inc": {"quantity": 1}}
        )
    else:
        await purchases_col.insert_one({
            "player_id": req.player_id,
            "item_id": req.item_id,
            "item_name": item["name"],
            "item_icon": item["icon"],
            "item_rarity": item["rarity"],
            "price_paid": item["price"],
            "quantity": 1,
            "purchased_at": datetime.utcnow(),
        })

    return {
        "success": True,
        "message": f"'{item['name']}' başarıyla satın alındı!",
        "new_sp_balance": new_balance,
        "item_name": item["name"],
    }


@app.get("/api/categories")
async def get_categories():
    """Tüm kategorileri getir"""
    categories = await items_col.distinct("category")
    return ["Tümü"] + sorted(categories)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "MMORPG Store API"}