export interface Vector {
  x: number;
  y: number;
}

export interface Projectile {
  id: string;
  position: Vector;
  velocity: Vector;
  radius: number;
  damage: number;
  bonusShieldDamage: number;
  bonusHullDamage: number;
  teamId?: string;
}

export interface Debris {
  id: string;
  position: Vector;
  velocity: Vector;
  radius: number;
  damage: number;
  bonusShieldDamage: number;
  bonusHullDamage: number;
  teamId?: string;
  debrisType?: DebrisType;
}

export enum ActionTypes {
  TURRET_ROTATE = "TURRET_ROTATE",
  TURRET_LOOK_AT = "TURRET_LOOK_AT",
  TURRET_CHARGE = "TURRET_CHARGE",
  TURRET_SHOOT = "TURRET_SHOOT",
  SHIP_ROTATE = "SHIP_ROTATE",
  SHIP_LOOK_AT = "SHIP_LOOK_AT",
  RADAR_SCAN = "RADAR_SCAN",
  CREW_MOVE = "CREW_MOVE",
}

export type Action = ActionTurretRotate | ActionTurretLookAt | ActionTurretCharge | ActionTurretShoot | ActionRadarScan | ActionCrewMove | ActionShipLookAt | ActionShipRotate;

export interface ActionTurretRotate extends StationAction {
  type: ActionTypes.TURRET_ROTATE;
  angle: number;
}

export interface ActionTurretLookAt extends StationAction {
  type: ActionTypes.TURRET_LOOK_AT;
  target: Vector;
}

export interface ActionTurretCharge extends StationAction {
  type: ActionTypes.TURRET_CHARGE;
}

export interface ActionTurretShoot extends StationAction {
  type: ActionTypes.TURRET_SHOOT;
}

export interface ActionShipRotate extends ActionBase {
  type: ActionTypes.SHIP_ROTATE;
  angle: number;
}

export interface ActionShipLookAt extends ActionBase {
  type: ActionTypes.SHIP_LOOK_AT;
  target: Vector;
}

export interface ActionRadarScan extends StationAction {
  type: ActionTypes.RADAR_SCAN;
  targetShip: string;
}

export interface ActionCrewMove extends ActionBase {
  type: ActionTypes.CREW_MOVE;
  crewMemberId: string;
  destination: Vector;
}

interface StationAction extends ActionBase {
  stationId: string;
}

interface ActionBase {
  type: ActionTypes;
}

export enum DebrisType {
  Large = "LARGE",
  Medium = "MEDIUM",
  Small = "SMALL",
}

export interface DebrisInfos {
  radius: number;
  damage: number;
  approximateSpeed: number;
  explodesInto: {
    debrisType: DebrisType;
    approximateAngle: number;
  };
}

export enum TurretType {
  Normal = 'NORMAL',
  Fast = 'FAST',
  Cannon = 'CANNON',
  Sniper = 'SNIPER',
  EMP = 'EMP',
}

interface TurretInfos {
  rotatable: boolean;
  rocketChargeCost: number;
  maxCharge: number;
  rocketSpeed: number;
  rocketRadius: number;
  rocketDamage: number;
  rocketBonusShieldDamage: number;
  rocketBonusHullDamage: number;
}

interface ShieldInfos {
  shieldRadius: number;
  shieldRegenerationPercent: number;
  shieldBreakHandicap: number;
}

interface RadarInfos {
  radarRadius: number;
}

export interface StationInfos {
  turretInfos: { [k: string]: TurretInfos };
  shield: ShieldInfos;
  radar: RadarInfos;
}

export interface ShipInfos {
  grid: {
    height: number;
    width: number;
  };
  maxHealth: number;
  maxShield: number;
  maxRotationDegrees: number;
  stations: StationInfos;
}

export interface StationDistance {
  stationId: string;
  stationPosition: Vector;
  distance: number;
}

export interface Station {
  id: string;
  gridPosition: Vector;
  operator?: string;
}

export interface TurretStation extends Station {
  worldPosition: Vector;
  orientationDegrees: number;
  turretType?: TurretType;
  charge: number;
  cooldown: number;
  currentTarget?: string;
}

export interface RadarStation extends Station {
  currentTarget?: string;
}

export interface Crew {
  id: string;
  name: string;
  age: number;
  sociaInsurance: string;
  currentStation: string | null;
  destination: Vector | null;
  gridPosition: Vector;
  distanceFromStations: {
    turrets: StationDistance[];
    shields: StationDistance[];
    radars: StationDistance[];
    helms: StationDistance[];
  };
}

export interface Ship {
  teamId: string;
  worldPosition: Vector;
  orientationDegrees: number;
  currentHealth: number;
  currentShield: number;
  crew: Crew[];
  walkableTiles: Vector[];
  stations: {
    turrets: TurretStation[];
    shields: Station[];
    radars: RadarStation[];
    helms: Station[]
  };
}

export interface GameTick {
  type: string;
  lastTickErrors: string[];
  constants: {
    world: {
      width: number;
      height: number;
    };
    debrisInfos: { [k in DebrisType]: DebrisInfos };
    ship: ShipInfos;
  };
  currentTickNumber: number;
  debris: Debris[];
  rockets: Projectile[];
  shipsPositions: { [id: string]: Vector };
  ships: { [id: string]: Ship };
  currentTeamId: string;
}

export class GameMessage implements GameTick {
  public readonly type: string;
  public readonly lastTickErrors: string[];
  public readonly constants: {
    world: {
      width: number;
      height: number;
    };
    debrisInfos: { [k in DebrisType]: DebrisInfos };
    ship: ShipInfos;
  };
  public readonly currentTickNumber: number;
  public readonly debris: Debris[];
  public readonly rockets: Projectile[];
  public readonly shipsPositions: { [k: string]: Vector };
  public readonly ships: { [k: string]: Ship };
  public readonly currentTeamId: string;

  constructor(rawTick: GameTick) {
    Object.assign(this, rawTick);
  }
}
