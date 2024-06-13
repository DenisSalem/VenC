/*
 * Copyright 2016, 2023 Denis Salem
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
 
var VENC_ON_LOAD_CALLBACK_REGISTER = [];

function VENC_ON_LOAD_CALLBACK() {
    var i;
    for (i = 0; i < VENC_ON_LOAD_CALLBACK_REGISTER.length; i++) {
        VENC_ON_LOAD_CALLBACK_REGISTER[i]();
    }
}

window.onload = VENC_ON_LOAD_CALLBACK;
