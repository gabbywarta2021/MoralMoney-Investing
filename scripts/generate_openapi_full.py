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
"""Placeholder generator

The original generator contained a large literal and caused lint/syntax noise.
Keep a small helper that copies `openapi_full.json` to the working file if present.
"""
import json
import os


def main():
    here = os.path.dirname(__file__)
    full = os.path.join(here, '..', 'openapi_full.json')
    if not os.path.exists(full):
        print('openapi_full.json not found; nothing to generate')
        return
    with open(full, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    with open(os.path.join(here, '..', 'openapi.json'), 'w', encoding='utf-8') as out:
        json.dump(spec, out, indent=2, ensure_ascii=False)
    print('WROTE openapi.json from openapi_full.json')


if __name__ == '__main__':
    main()
# Providers
