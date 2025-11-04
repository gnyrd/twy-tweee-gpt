#!/bin/bash
# Switch between test and production Mailchimp configurations

if [ "$1" == "test" ]; then
    echo "Switching to TEST environment..."
    cp .env.mailchimp.test .env.mailchimp
    echo "✅ Using TEST audience (e1cfd6e694)"
elif [ "$1" == "prod" ]; then
    echo "⚠️  Switching to PRODUCTION environment..."
    cp .env.mailchimp.prod .env.mailchimp
    echo "✅ Using PRODUCTION audience"
else
    echo "Usage: ./switch_mailchimp_env.sh [test|prod]"
    echo ""
    echo "Current active config:"
    if [ -f .env.mailchimp ]; then
        grep "MAILCHIMP_AUDIENCE_ID" .env.mailchimp
    else
        echo "No active config found"
    fi
fi
