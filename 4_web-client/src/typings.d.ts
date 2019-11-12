/* SystemJS module definition */
declare var module: NodeModule;
interface NodeModule {
  id: string;
}

interface JQuery {
  sideNav: any;
  dropdown: any;
}

/**
 * Materialize module definition
 * see reference here '../../../assets/js/materialize';
 */
declare var M: Materialize
interface Materialize {
  Sidenav: any;
  Dropdown: any;
  FormSelect: any;
  Datepicker: any;
  Chips: any;
  toast: any;
  AutoInit: any;
  Collapsible: any;
}