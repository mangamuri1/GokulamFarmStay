import sys
with open('d:/Gokulam/css/main.css', 'a') as f:
    f.write('''
/* Logo Updates */
.logo img {
    background: transparent;
    object-fit: contain;
    padding: 0;
    margin: 0;
    border: none;
    box-shadow: none;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}
''')
