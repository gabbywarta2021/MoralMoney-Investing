import json

spec = {
  "openapi": "3.0.3",
  "info": {
    "title": "MoralMoney Investing API",
    "version": "0.1.0",
    "description": "Expanded API for the MVP: auth, providers, tags, instruments, preferences, watchlist, allocate."
  },
  "servers": [
    {"url": "https://api.example.com", "description": "Production"}
  ],
  "components": {
    "parameters": {
      "AuthorizationHeader": {
        "name": "Authorization",
        "in": "header",
        "description": "Bearer token",
        "required": False,
        "schema": {"type": "string"},
        "example": "Bearer <token>"
      }
    },
    "securitySchemes": {
      "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    },
    "schemas": {
      "User": {
        "type": "object",
        "properties": {
          "id": {"type": "integer"},
          "email": {"type": "string", "format": "email"},
          "risk_level": {"type": "string"},
          "is_admin": {"type": "boolean"},
          "created_at": {"type": "string", "format": "date-time"}
        }
      },
      "AuthRequest": {
        "type": "object",
        "properties": {"email": {"type": "string"}, "password": {"type": "string"}},
        "required": ["email", "password"]
      },
      "AuthResponse": {"type": "object", "properties": {"access_token": {"type": "string"}, "token_type": {"type": "string"}}},
      "Provider": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "base_url": {"type": "string"}, "notes": {"type": "string"}}, "required": ["name", "base_url"]},
      "Tag": {"type": "object", "properties": {"id": {"type": "integer"}, "name": {"type": "string"}, "category": {"type": "string"}, "description": {"type": "string"}}},
      "Instrument": {"type": "object", "properties": {"id": {"type": "integer"}, "ticker": {"type": "string"}, "name": {"type": "string"}, "provider_id": {"type": "integer"}}},
      "Preference": {"type": "object", "properties": {"id": {"type": "integer"}, "user_id": {"type": "integer"}, "tag_id": {"type": "integer"}, "type": {"type": "string", "enum": ["inclusion", "exclusion"]}, "strength": {"type": "integer"}}},
      "WatchlistEntry": {"type": "object", "properties": {"id": {"type": "integer"}, "user_id": {"type": "integer"}, "instrument_id": {"type": "integer"}}},
      "AllocationResult": {"type": "object", "properties": {"user_id": {"type": "integer"}, "risk_level": {"type": "string"}, "cash_pct": {"type": "number"}, "items": {"type": "array", "items": {"type": "object"}}}},
      "Error": {"type": "object", "properties": {"detail": {"type": "string"}}}
    }
  },
  "paths": {}
}

p = spec["paths"]

# Auth
p["/api/v1/auth/register"] = {
  "post": {
    "summary": "Register new user",
    "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuthRequest"}}}},
    "responses": {
      "201": {"description": "User created", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}},
      "400": {"description": "Bad request", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Error"}}}}
    }
  }
}

p["/api/v1/auth/login"] = {
  "post": {
    "summary": "Login and receive token",
    "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuthRequest"}}}},
    "responses": {
      "200": {"description": "Token", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AuthResponse"}}}},
      "401": {"description": "Unauthorized"}
    }
  }
}

# Providers
p["/api/v1/providers"] = {
  "get": {
    "summary": "List providers",
    "responses": {"200": {"description": "Providers list", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Provider"}}}}}}
}

p["/api/v1/providers/{providerId}"] = {
  "put": {
    "summary": "Update provider (admin)",
    "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}, {"name": "providerId", "in": "path", "required": True, "schema": {"type": "integer"}}],
    "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Provider"}}}},
    "responses": {"200": {"description": "Updated"}, "403": {"description": "Forbidden"}}
  },
  "delete": {
    "summary": "Delete provider (admin)",
    "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}, {"name": "providerId", "in": "path", "required": True, "schema": {"type": "integer"}}],
    "responses": {"204": {"description": "Deleted"}, "403": {"description": "Forbidden"}}
  }
}

p["/api/v1/providers/{providerId}/sync"] = {
  "post": {
    "summary": "Trigger provider sync",
    "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}, {"name": "providerId", "in": "path", "required": True, "schema": {"type": "integer"}}],
    "requestBody": {"required": False, "content": {"application/json": {"schema": {"type": "object", "properties": {"full": {"type": "boolean", "default": False}}}}}},
    "responses": {"202": {"description": "Sync started", "content": {"application/json": {"schema": {"type": "object", "properties": {"task_id": {"type": "string"}}}}}}}
}

# Tags
p["/api/v1/tags"] = {
  "get": {"summary": "List tags", "responses": {"200": {"description": "Tags list", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Tag"}}}}}}},
  "post": {"summary": "Create tag", "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}}}, "responses": {"201": {"description": "Created"}}}

# Instruments
p["/api/v1/instruments"] = {
  "get": {"summary": "List instruments", "responses": {"200": {"description": "Instruments", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Instrument"}}}}}}},
  "post": {"summary": "Create instrument", "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Instrument"}}}}, "responses": {"201": {"description": "Created"}}}

# Preferences
p["/api/v1/users/me/preferences"] = {
  "get": {"summary": "Get current user's preferences", "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}], "responses": {"200": {"description": "Preferences list", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/Preference"}}}}}}},
  "post": {"summary": "Add preference for current user", "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}], "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Preference"}}}}, "responses": {"200": {"description": "Created"}}}

# Watchlist
p["/api/v1/users/me/watchlist"] = {
  "get": {"summary": "Get current user's watchlist", "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}], "responses": {"200": {"description": "Watchlist", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/WatchlistEntry"}}}}}}},
  "post": {"summary": "Add to watchlist", "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}], "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/WatchlistEntry"}}}}, "responses": {"200": {"description": "Added"}}}

# Allocate
p["/api/v1/allocate"] = {
  "post": {"summary": "Get allocation suggestion", "parameters": [{"$ref": "#/components/parameters/AuthorizationHeader"}], "requestBody": {"required": True, "content": {"application/json": {"schema": {"type": "object", "properties": {"user_id": {"type": "integer"}, "risk_level": {"type": "string"}}}}}}, "responses": {"200": {"description": "Allocation result", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/AllocationResult"}}}}}

spec["paths"] = p

with open("openapi_full.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print("generated openapi_full.json")
