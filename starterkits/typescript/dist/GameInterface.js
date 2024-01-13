"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.GameMessage = exports.TurretType = exports.DebrisType = exports.ActionTypes = void 0;
var ActionTypes;
(function (ActionTypes) {
    ActionTypes["TURRET_ROTATE"] = "TURRET_ROTATE";
    ActionTypes["TURRET_LOOK_AT"] = "TURRET_LOOK_AT";
    ActionTypes["TURRET_CHARGE"] = "TURRET_CHARGE";
    ActionTypes["TURRET_SHOOT"] = "TURRET_SHOOT";
    ActionTypes["SHIP_ROTATE"] = "SHIP_ROTATE";
    ActionTypes["SHIP_LOOK_AT"] = "SHIP_LOOK_AT";
    ActionTypes["RADAR_SCAN"] = "RADAR_SCAN";
    ActionTypes["CREW_MOVE"] = "CREW_MOVE";
})(ActionTypes = exports.ActionTypes || (exports.ActionTypes = {}));
var DebrisType;
(function (DebrisType) {
    DebrisType["Large"] = "LARGE";
    DebrisType["Medium"] = "MEDIUM";
    DebrisType["Small"] = "SMALL";
})(DebrisType = exports.DebrisType || (exports.DebrisType = {}));
var TurretType;
(function (TurretType) {
    TurretType["Normal"] = "NORMAL";
    TurretType["Fast"] = "FAST";
    TurretType["Cannon"] = "CANNON";
    TurretType["Sniper"] = "SNIPER";
    TurretType["EMP"] = "EMP";
})(TurretType = exports.TurretType || (exports.TurretType = {}));
class GameMessage {
    constructor(rawTick) {
        Object.assign(this, rawTick);
    }
}
exports.GameMessage = GameMessage;
//# sourceMappingURL=GameInterface.js.map