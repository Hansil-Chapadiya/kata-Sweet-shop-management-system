import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { ConfirmDialogComponent } from '../confirm-dialog/confirm-dialog.component';
import { MatDialog } from '@angular/material/dialog';
import { NgForm } from '@angular/forms';
import Swal from 'sweetalert2';

interface Sweet {
  _id: string;
  name: string;
  category: string;
  price: number;
  quantity: number;
  discount: number;
  description: string;
  image_url: string;
  is_available: boolean;
}

interface PurchaseItem {
  sweet_id: string;
  quantity: number;
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  sweets: Sweet[] = [];
  loading = true;
  error = '';

  // Modal controls
  showAddModal = false;
  showRestockModal = false;
  showPurchaseModal = false;

  // Selected items
  selectedSweet: Sweet | null = null;
  selectedSweetForPurchase: Sweet | null = null;

  // Form values
  restockQuantity = 0;
  purchaseQuantity = 1;
  purchaseItems: PurchaseItem[] = [];

  searchQuery: string = '';
  sortBy: string = 'name';
  sortOrder: string = 'asc';
  categoryFilter: string = '';
  categories: string[] = [];

  newSweet: Partial<Sweet> = {
    name: '',
    category: '',
    price: 0,
    quantity: 0,
    discount: 0,
    description: '',
    image_url: '',
    is_available: true
  };

  private baseUrl = 'https://kata-sweet-shop-management-system.onrender.com';
  private apiHeaders = new HttpHeaders({
    'Content-Type': 'application/json',
    'API-Key': '1234567890'
  });

  constructor(private http: HttpClient, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.fetchSweets();
    this.searchSweets();
  }

  // Replace your existing fetchSweets with this version
  fetchSweets(): void {
    this.loading = true;

    this.http.get<{ status: boolean, sweets: Sweet[] }>(
      `${this.baseUrl}/searchsweets`,
      {
        headers: this.apiHeaders,
        params: {
          query: '',
          sort_by: 'name',
          order: 'asc'
        }
      }
    ).subscribe({
      next: (response) => {
        if (response.status && response.sweets) {
          this.sweets = response.sweets;
          this.initializeCategories();
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load sweets. Please try again later.';
        this.loading = false;
        console.error('Error fetching sweets:', err);
        Swal.fire({
          icon: 'error',
          title: 'Not Found',
          text: 'Error for fetching Sweets!',
          confirmButtonColor: '#e74c3c'
        });
      }
    });
  }

  calculateDiscountedPrice(price: number, discount: number): number {
    return price - (price * discount / 100);
  }

  // Add Sweet Methods
  openAddSweetModal(): void {
    this.showAddModal = true;
  }

  closeAddModal(): void {
    this.showAddModal = false;
    this.resetNewSweet();
  }

  addSweet(form: NgForm): void {
    // Mark all fields as touched to show validation messages
    Object.keys(form.controls).forEach(field => {
      const control = form.controls[field];
      control.markAsTouched({ onlySelf: true });
    });

    if (form.invalid) {
      // Optionally show a Swal alert for general form error
      Swal.fire({
        icon: 'error',
        title: 'Form Invalid',
        text: 'Please fix all errors before submitting',
        confirmButtonColor: '#e74c3c'
      });
      return;
    }

    this.http.post<{ status: boolean, sweet_id: string, message: string }>(
      `${this.baseUrl}/addsweet`,
      this.newSweet,
      { headers: this.apiHeaders }
    ).subscribe({
      next: (response) => {
        if (response.status) {
          this.fetchSweets();
          this.closeAddModal();
          Swal.fire({
            icon: 'success',
            title: 'Sweet Added',
            text: 'The sweet was added successfully.',
            confirmButtonColor: '#43a047'
          });
        }
      },
      error: (err) => {
        console.error('Error adding sweet:', err);
        const errorMsg = err.error?.detail?.message || 'Something went wrong while purchasing.';
        Swal.fire({
          icon: 'error',
          title: 'Sweet not added',
          text: errorMsg,
          confirmButtonColor: '#e74c3c'
        });
      }
    });
  }

  private resetNewSweet(): void {
    this.newSweet = {
      name: '',
      category: '',
      price: 0,
      quantity: 0,
      discount: 0,
      description: '',
      image_url: '',
      is_available: true
    };
  }

  // Restock Methods
  openRestockModal(sweet: Sweet): void {
    this.selectedSweet = sweet;
    this.restockQuantity = 0;
    this.showRestockModal = true;
  }

  closeRestockModal(): void {
    this.showRestockModal = false;
    this.selectedSweet = null;
  }

  restockSweet(): void {
    if (!this.selectedSweet) return;

    this.http.post<{ status: boolean, message: string, updated_stock: number }>(
      `${this.baseUrl}/restock`,
      {
        quantity: this.restockQuantity,
        sweet_id: this.selectedSweet._id
      },
      { headers: this.apiHeaders }
    ).subscribe({
      next: (response) => {
        if (response.status) {
          this.fetchSweets();
          this.closeRestockModal();
        }
      },
      error: (err) => {
        console.error('Error restocking:', err);
        const errorMsg = err.error?.detail?.message || 'Something went wrong while purchasing.';
        Swal.fire({
          icon: 'error',
          title: 'Sweet not restocked',
          text: errorMsg,
          confirmButtonColor: '#e74c3c'
        });
      }
    });
  }

  // Purchase Methods
  openPurchaseModal(sweet: Sweet): void {
    this.selectedSweetForPurchase = sweet;
    this.purchaseQuantity = 1;
    this.showPurchaseModal = true;
  }

  closePurchaseModal(): void {
    this.showPurchaseModal = false;
    this.selectedSweetForPurchase = null;
  }

  addToPurchaseCart(): void {
    const existing = this.purchaseItems.find(item => item.sweet_id === this.selectedSweetForPurchase?._id);
    if (existing) {
      existing.quantity += this.purchaseQuantity;
    } else {
      this.purchaseItems.push({
        sweet_id: this.selectedSweetForPurchase!._id,
        quantity: this.purchaseQuantity
      });
    }

    this.closePurchaseModal();
  }

  getTotalItems(): number {
    return this.purchaseItems.reduce((total, item) => total + item.quantity, 0);
  }

  purchaseSweet(): void {
    if (!this.purchaseItems.length) return;

    this.http.post<{
      status: boolean,
      message: string,
      results: Array<{
        status: boolean,
        message: string,
        remaining_quantity: number
      }>
    }>(
      `${this.baseUrl}/purchase`,
      { items: this.purchaseItems },
      { headers: this.apiHeaders }
    ).subscribe({
      next: (response) => {
        if (response.status) {
          this.fetchSweets();
          this.purchaseItems = [];
          Swal.fire({
            icon: 'success',
            title: 'Purchase Complete!',
            text: 'Sweets were successfully purchased.',
            confirmButtonColor: '#43a047',
          });
        }
      },
      error: (err) => {
        console.error('Error purchasing:', err);
        const errorMsg = err.error?.detail?.message || 'Something went wrong while purchasing.';
        Swal.fire({
          icon: 'error',
          title: 'Purchase Failed',
          text: errorMsg,
          confirmButtonColor: '#e74c3c',
        });
      }
    });
  }

  removePurchaseItem(index: number): void {
    this.purchaseItems.splice(index, 1);
  }

  getSweetName(sweetId: string): string {
    const sweet = this.sweets.find(s => s._id === sweetId);
    return sweet ? sweet.name : 'Unknown';
  }

  // Delete Methods
  confirmDelete(sweetId: string): void {
    const dialogRef = this.dialog.open(ConfirmDialogComponent, {
      data: {
        title: 'Delete Sweet',
        message: 'Are you sure you want to delete this sweet?'
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.deleteSweet(sweetId);
      }
    });
  }

  deleteSweet(sweetId: string): void {
    this.http.delete<{ status: boolean, message: string }>(
      `${this.baseUrl}/deletesweet/${sweetId}`,
      { headers: this.apiHeaders }
    ).subscribe({
      next: (response) => {
        if (response.status) {
          this.fetchSweets();
          Swal.fire({
            icon: 'success',
            title: 'Sweet Deleted',
            text: 'The sweet was removed successfully.',
            confirmButtonColor: '#F44336'
          });
        }
      },
      error: (err) => {
        console.error('Error deleting sweet:', err);
        const errorMsg = err.error?.detail?.message || 'Something went wrong while purchasing.';
        Swal.fire({
          icon: 'success',
          title: 'Sweet not deleted',
          text: errorMsg,
          confirmButtonColor: '#43a047'
        });
      }
    });
  }

  initializeCategories(): void {
    // Extract unique categories from sweets
    this.categories = [...new Set(this.sweets.map(sweet => sweet.category))];
  }

  searchSweets(): void {
    this.loading = true;

    const params = {
      query: this.searchQuery,
      sort_by: this.sortBy,
      order: this.sortOrder,
      category: this.categoryFilter
    };

    this.http.get<{ status: boolean, sweets: Sweet[] }>(
      `${this.baseUrl}/searchsweets`,
      {
        headers: this.apiHeaders,
        params: params
      }
    ).subscribe({
      next: (response) => {
        if (response.status && response.sweets) {
          this.sweets = response.sweets;
          this.initializeCategories(); // Update available categories
        }
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load sweets. Please try again later.';
        this.loading = false;
        console.error('Error searching sweets:', err);
      }
    });
  }

}