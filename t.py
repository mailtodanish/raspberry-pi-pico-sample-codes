import lcddriver
display = lcddriver.lcd()
display.lcd_clear()
display.lcd_display_string("ABCDEFGHIJ", 1)
display.lcd_display_string("123456789", 2)