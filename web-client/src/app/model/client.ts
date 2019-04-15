export class Client {
    constructor(
        rot_x: number,
        rot_y: number,
        rot_z: number,
        s_x: number,
        s_y: number,
        s_z: number,
        t_x: number,
        t_y: number,
        t_z: number) {

        this.rot_x = rot_x;
        this.rot_y = rot_y;
        this.rot_z = rot_z;
        this.s_x = s_x;
        this.s_y = s_y;
        this.s_z = s_z;
        this.t_x = t_x;
        this.t_y = t_y;
        this.t_z = t_z;

    }

    rot_x: number;
    rot_y: number;
    rot_z: number;
    s_x: number;
    s_y: number;
    s_z: number;
    t_x: number;
    t_y: number;
    t_z: number;
}