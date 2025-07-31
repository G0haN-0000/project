#!/bin/bash
pg_dump -U rezerwacja_user rezerwacja_db > ~/rezerwacja_$(date +%F).sql
