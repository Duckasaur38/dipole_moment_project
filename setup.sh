mkdir -p ~/.streamlit/
echo “\
[general]\n\
email = \”zoe_shleifer22@milton.edu\”\n\
“ > ~/.streamlit/credentials.toml
echo “\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
“ > ~/.streamlit/config.toml