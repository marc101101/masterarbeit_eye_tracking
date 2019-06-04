import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ConfigComponent } from './config/config.component';
import { HomeComponent } from './home/home.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { AnnotateComponent } from './annotate/annotate.component';
import { VisualizerComponent } from './visualizer/visualizer.component';

const routes: Routes = [
  { 
    path: '', 
    redirectTo: '/home', 
    pathMatch: 'full'
  },
  { 
    path: 'home', 
    component: HomeComponent 
  },
  { 
    path: 'config', 
    component: ConfigComponent 
  },
  { 
    path: 'annotate', 
    component: AnnotateComponent 
  },
  { 
    path: 'visualizer', 
    component: VisualizerComponent 
  },
  { 
    path: '**', 
    component: PageNotFoundComponent 
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
