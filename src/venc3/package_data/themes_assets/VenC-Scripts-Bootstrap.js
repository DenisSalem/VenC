/*
 * Copyright 2016, 2024 Denis Salem
 * 
 * This file is part of VenC.
 * 
 * VenC is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.

 * VenC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with VenC.  If not, see <http://www.gnu.org/licenses/>.
 */
VENC_SCRIPT_BOOTSTRAP = {
    version: "1.0.0",
    callbacks_register: [],
    third_party_on_load: window.onload,
    venc_on_load: function VENC_ON_LOAD_CALLBACK() {
        if (VENC_SCRIPT_BOOTSTRAP.third_party_on_load !== null) {
            VENC_SCRIPT_BOOTSTRAP.third_party_on_load();
        }
        
        var i;
        for (i = 0; i < VENC_SCRIPT_BOOTSTRAP.callbacks_register.length; i++) {
            VENC_SCRIPT_BOOTSTRAP.callbacks_register[i]();
        }
    }
};
 
window.onload = VENC_SCRIPT_BOOTSTRAP.venc_on_load;
